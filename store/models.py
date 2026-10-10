from django.db import models
from accounts.models import SellerProfile


class Store(models.Model):
    seller = models.OneToOneField(
        SellerProfile,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(default=0)

    is_active=models.BooleanField(default=True)
    
    # image = models.ImageField(
    #     upload_to="products/",
    #     blank=True,
    #     null=True
    # )

    def __str__(self):
        return self.name
        