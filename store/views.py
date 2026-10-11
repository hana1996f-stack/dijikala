
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProductForm, StoreForm
from .models import Product, Store


def home(request):
    products = Product.objects.filter(
        is_active=True
    ).order_by("-id")

    return render(
        request,
        "home.html",
        {"products": products},
    )


@login_required
def create_store(request):
    if hasattr(request.user, "customerprofile"):
        return redirect("customer_panel")

    seller = getattr(request.user, "sellerprofile", None)

    if seller is None:
        return redirect("login")

    if Store.objects.filter(seller=seller).exists():
        return redirect("seller_panel")

    if request.method == "POST":
        form = StoreForm(request.POST)

        if form.is_valid():
            store = form.save(commit=False)
            store.seller = seller
            store.save()

            return redirect("seller_panel")
    else:
        form = StoreForm()

    return render(
        request,
        "store/create_store.html",
        {"form": form},
    )


def store_list(request):
    stores = Store.objects.all().order_by("-id")

    return render(
        request,
        "stores.html",
        {"stores": stores},
    )


def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    is_owner = (
        request.user.is_authenticated
        and store.seller.user_id == request.user.id
    )

    if is_owner:
        products = Product.objects.filter(store=store)
    else:
        products = Product.objects.filter(
            store=store,
            is_active=True,
        )

    return render(
        request,
        "store_detail.html",
        {
            "store": store,
            "products": products,
        },
    )


@login_required
def add_product(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if store.seller.user != request.user:
        raise Http404

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()

            return redirect(
                "store_detail",
                store_id=store.id,
            )
    else:
        form = ProductForm()

    products = Product.objects.filter(store=store)

    return render(
        request,
        "store_detail.html",
        {
            "store": store,
            "products": products,
            "form": form,
        },
    )


@login_required
@require_POST
def toggle_product_active(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("store__seller__user"),
        id=product_id,
    )

    if product.store.seller.user_id != request.user.id:
        raise Http404

    product.is_active = not product.is_active
    product.save(update_fields=["is_active"])

    if product.is_active:
        messages.success(
            request,
            "Product activated successfully.",
        )
    else:
        messages.success(
            request,
            "Product deactivated successfully.",
        )

    return redirect(
        "store_detail",
        store_id=product.store_id,
    )
