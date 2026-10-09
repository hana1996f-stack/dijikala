from django.contrib.auth import login, logout  
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required

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
            login(request, user)
            return redirect("/customer/")

    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    )
@login_required
def logout_view(request): 
    logout(request)
    return render( request, "accounts/logout.html" )

@login_required
def customer_panel(request) :
    return render (request,"accounts/customer_panel.html")

@login_required
def seller_panel(request) :
    if not hasattr(request.user ,"seller profile"):
        return redirect ("login")
    seller=request.user.sellerprofile
    store=getattr(seller,"store" , None)
    return render (request,"accounts/seller_panel.html")

    