from django import forms 
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

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
    email = forms.EmailField(
        required=True
    )
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email