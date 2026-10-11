
from django.contrib.auth import login, logout  
from django.contrib.auth import login, logout
from django.http import request
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile
from decimal import Decimal
from django.contrib import messages
from django import forms

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            from django.contrib.auth import authenticate

            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect("/admin/")

                if hasattr(user, "sellerprofile"):
                    return redirect("/seller/")

                if hasattr(user, "customerprofile"):
                    return redirect("/customer/")

                logout(request)

                form.add_error(
                    None,
                    "No role has been assigned to this account."
                )

            else:
                form.add_error(
                    None,
                    "Invalid username or password."
                )

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            role = form.cleaned_data["role"]

            if role == "customer":
                CustomerProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data["phone"],
                )
                login(request, user)
                return redirect("/customer/")

            elif role == "seller":
                from .models import SellerProfile

                SellerProfile.objects.create(user=user)
                login(request, user)
                return redirect("/seller/")

    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/signup.html",
        {"form": form},
    )


@login_required
def logout_view(request):
    logout(request)
    return render( request, "accounts/logout.html" )

@login_required
def customer_panel(request) :
    customer=getattr(request.user, "customerprofile", None)
    if customer is None:
        return redirect("login")
    return render (request,"accounts/customer_panel.html" ,  {"customer" :customer} , )

@login_required
def seller_panel(request) :
    if not hasattr(request.user ,"sellerprofile"):
        return redirect ("login")
    seller=request.user.sellerprofile
    store=getattr(seller,"store" , None)


    return render(request, "accounts/seller_panel.html", {"store": store})


class BalanceForm(forms.Form):
    amount = forms.DecimalField(
        min_value=Decimal("1.00"),
        max_digits=12,
        decimal_places=2,
        label="Amount",
    )


@login_required
def payment_view(request):
    customer = getattr(request.user, "customerprofile", None)
    if customer is None:
        return redirect("login")

    if request.method == "POST":
        form = BalanceForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]
            customer.balance += amount
            customer.save(update_fields=["balance"])

            messages.success(
                request,
                "Your balance has been increased successfully.",
            )
            return redirect("customer_panel")
    else:
        form = BalanceForm()

    return render(
        request,
        "accounts/payment.html",
        {"form": form, "customer": customer},
    )
