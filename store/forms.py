from django import forms
from .models import Store, Product


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            "name",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            # "image",
            "stock",
        ]

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )
        return price