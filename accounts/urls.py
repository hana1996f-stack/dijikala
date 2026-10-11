from django.urls import path
from .views import login_view, logout_view, signup_view, customer_panel, seller_panel, payment_view


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup_view , name="signup"),
    path("customer/" , customer_panel  , name = "customer_panel" ) ,
    path("seller/" , seller_panel  , name = "seller_panel" ),
    path("payment/", payment_view, name="payment"),
    
]