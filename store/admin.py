from django.contrib import admin
from .models import Store, Product


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "seller",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "store",
        "price",
        "stock",
        "is_active" ,
    )
    list_filter = (
        "is_active" , "store", )
    
    list_editable = ("is_active",)
