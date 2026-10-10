from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import CustomerProfile, SellerProfile
from cart.models import CartItem
from store.models import Product
from .models import Order, OrderItem

@login_required
def checkout (request):
    customer = get_object_or_404(CustomerProfile, user=request.user,)
    
    cart_items= CartItem.objects.filter(customer=customer).select_related('product','product__store')
    
    inactive_items = cart_items.filter(product__is_active=False)
    
    if inactive_items.exists():
        inactive_product_names = list(inactive_items.values_list('product__name', flat=True))

        inactive_items.delete()

        messages.error(request,
            f"The following products are no longer available and have been removed from your cart: {', '.join(inactive_product_names)}")

        return redirect("cart:detail")
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart:detail')
    
    total = sum((item.subtotal for item in cart_items), Decimal("0.00"))
    
        
    
    
    with transaction.atomic():
        #AI Lock products to prevent concurrent stock updates
        
        customer = CustomerProfile.objects.select_for_update().get(id=customer.id)

        products = Product.objects.select_for_update().filter(id__in=[item.product_id for item in cart_items])
        products_by_id = {product.id: product for product in products}
        
        # missing_items = [item for item in cart_items
        #     if item.product_id not in products_by_id]

        # missing_product_names = [item.product.name for item in missing_items]
        
        # if missing_items:
        #     CartItem.objects.filter(id__in=[item.id for item in missing_items]).delete()

        #     messages.error(request,
        #                    f"The following products are no longer available and have been removed from your cart: {', '.join(missing_product_names)}")
        #     return redirect("cart:detail")

        
        total = sum((products_by_id[item.product_id].price * item.quantity for item in cart_items),Decimal("0.00"))
        
        if customer.balance < total:
            messages.error (request, "You do not have enough balance to complete this order.")
            return redirect('cart:detail')
        
        for item in cart_items:
            product = products_by_id[item.product_id]

            if item.quantity > product.stock:
                messages.error(request,f"Not enough stock for {product.name}.")
                return redirect("cart:detail")
            
            
        seller_ids = {product.store.seller_id for product in products_by_id.values()}
        sellers = SellerProfile.objects.select_for_update().filter(id__in=seller_ids)
        sellers_by_id = {seller.id: seller for seller in sellers}
        
        
        order = Order.objects.create(customer=customer,total_amount=total,)
        
        for item in cart_items:
            
            product = products_by_id[item.product_id]
            
            OrderItem.objects.create(
                order=order,
                product = products_by_id[item.product_id],
                quantity=item.quantity,
                price=product.price,)
            
            product.stock -= item.quantity
            product.save(update_fields=["stock"])
            
            seller = sellers_by_id[product.store.seller_id]
            seller.balance += product.price * item.quantity
            seller.save(update_fields=["balance"])
            
        customer.balance -= total
        customer.save(update_fields=["balance"])
        
        cart_items.delete()
    messages.success(request, "Your order has been placed successfully!")
    return redirect("customer_panel")