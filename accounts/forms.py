from django import forms 
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(
                username=username,
                password=password
            )

            if user is None:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            self.user = user
        return cleaned_data

class SignUpForm(UserCreationForm):
    phone = forms.CharField (label="phone number" , max_length=15 , required=True)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_phone(self):
        phone= self.cleaned_data["phone"].strip ()
        if not phone.isdigit():
            raise forms.ValidationError ("please inter a valid phone number.")
        if CustomerProfile.objects.filter(phone=phone).exists() :
            raise forms.ValidationError ("an account with this phone number already exists.")
        return phone


