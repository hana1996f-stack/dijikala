
from django.urls import path

from .views import (
    home,
    store_list,
    store_detail,
    add_product,
    create_store,
    toggle_product_active,
)


urlpatterns = [
    path("", home, name="home"),

    path(
        "stores/",
        store_list,
        name="stores"
    ),

    path(
        "stores/<int:store_id>/",
        store_detail,
        name="store_detail"
    ),

    path(
        "stores/<int:store_id>/add-product/",
        add_product,
        name="add_product"
    ),

    path(
        "stores/create/",
        create_store,
        name="create_store"
    ),

    path(
        "products/<int:product_id>/toggle-active/",
        toggle_product_active,
        name="toggle_product_active"
    ),
]
