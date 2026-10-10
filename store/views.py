from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import SellerProfile

from .forms import ProductForm
from .models import Product, Store


def home(request):
    products = Product.objects.filter(is_active=True).order_by("-id")

    return render(
        request,
        "home.html",
        {"products": products}
    )


def store_list(request):
    stores = Store.objects.all().order_by("-id")

    return render(
        request,
        "stores.html",
        {"stores": stores}
    )


def store_detail(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id
    )

    products = Product.objects.filter(
        store=store ,
        is_active=True
    )

    return render(
        request,
        "store_detail.html",
        {
            "store": store,
            "products": products,
        }
    )


@login_required
def add_product(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id
    )

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
                store_id=store.id
            )

    else:
        form = ProductForm()

    return render(
        request,
        "store_detail.html",
        {
            "store": store,
            "products": Product.objects.filter(store=store ,is_active=True ,                                               ),
            "form": form,
        }
    )