
from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path ('' , include("store.urls")),
    path ('cart/' , include("cart.urls")),
    path ('orders/' , include("orders.urls"))
]
