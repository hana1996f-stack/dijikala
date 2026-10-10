from django.db import models
from accounts.models import CustomerProfile
from store.models import Product

class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.PROTECT, related_name="orders")
    total_amount= models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer}"
    
class OrderItem (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product= models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity= models.PositiveIntegerField(default=1)
    price= models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f'{self.product} X {self.quantity}'
    
    @property
    def subtotal(self):
        return self.price * self.quantity