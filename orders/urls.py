from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("history/", views.order_history, name="history"),
    path("receipt/<int:order_id>/", views.order_receipt, name="receipt"),
]