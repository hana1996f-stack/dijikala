from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import CartItem
from decimal import Decimal

from django.views.decorators.http import require_POST
from django.contrib import messages

from store.models import Product



@login_required
def cart_detail(request):
    customer = getattr(request.user, "customerprofile", None)
    if customer is None:
        return redirect("login")
    
    cart_items = CartItem.objects.filter(customer=customer).select_related("product", "product__store")
    total = sum((item.subtotal for item in cart_items), Decimal("0.00"))
    return render(request, "cart/cart_detail.html", {"cart_items": cart_items, "total": total,})


@login_required
@require_POST
def add_to_cart(request, product_id):
    customer = getattr(request.user, "customerprofile", None)
    
    if customer is None:
        return redirect("login")
    
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect("cart:detail")
    
    cart_item, created = CartItem.objects.get_or_create(customer=customer,product=product,defaults={"quantity": 1},)
    
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save(update_fields=["quantity"])
            
            
@login_required
@require_POST
def remove_from_cart(request, item_id):
    customer = getattr(request.user, "customerprofile", None)
    
    if customer is None:
            return redirect("login")
        
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    cart_item.delete()
    
    messages.success(request, "Product removed from your cart.")
    return redirect("cart:detail")