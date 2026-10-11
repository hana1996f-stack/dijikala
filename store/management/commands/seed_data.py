from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import SellerProfile, CustomerProfile
from store.models import Store, Product

class Command(BaseCommand):
    help = "Create test data for DIJIKALA"
    def handle(self, *args, **kwargs):

        # =========================
        # Create Sellers
        # =========================

        seller_names = [
            "seller_ali",
            "seller_sara",
            "seller_reza",
            "seller_mina",
        ]

        seller_profiles = []

        for username in seller_names:
            user, created = User.objects.get_or_create(
                username=username
            )

            if created:
                user.set_password("12345678")
                user.save()

            seller_profile, created = SellerProfile.objects.get_or_create(
                user=user
            )

            seller_profiles.append(seller_profile)

        # =========================
        # Create Customers
        # =========================

        customer_names = [
            "customer_ali",
            "customer_sara",
            "customer_reza",
            "customer_mina",
            "customer_hana",
        ]

        for username in customer_names:
            user, created = User.objects.get_or_create(
                username=username
            )

            if created:
                user.set_password("12345678")
                user.save()

            CustomerProfile.objects.get_or_create(
                user=user
            )

        # =========================
        # Create Stores
        # =========================



        stores_data = [
            ("Digital Store", seller_profiles[0]),
            ("Mobile Center", seller_profiles[1]),
            ("Laptop Market", seller_profiles[2]),
            ("Gadget Land", seller_profiles[3]),
        ]



        stores = []

        for name, seller in stores_data:
            store, created = Store.objects.get_or_create(
                seller=seller,
                defaults={
                    "name": name
                }
            )

            stores.append(store)

        # =========================
        # Create Products
        # =========================

        products_data = [
            (stores[0], "iPhone 15", 450000, 10),
            (stores[0], "iPhone 16", 580000, 8),
            (stores[0], "AirPods Pro", 120000, 20),
            (stores[0], "Apple Watch", 180000, 12),

            (stores[1], "Samsung Galaxy S24", 380000, 15),
            (stores[1], "Samsung Galaxy S25", 520000, 10),
            (stores[1], "Galaxy Buds", 85000, 25),
            (stores[1], "Samsung Watch", 150000, 10),

            (stores[2], "MacBook Air", 750000, 6),
            (stores[2], "MacBook Pro", 1100000, 4),
            (stores[2], "ASUS VivoBook", 420000, 8),
            (stores[2], "Lenovo ThinkPad", 550000, 7),

            (stores[3], "Xiaomi Watch", 90000, 18),
            (stores[3], "Xiaomi Band", 35000, 30),
            (stores[3], "Smart Home Camera", 70000, 15),
            (stores[3], "Smart Speaker", 60000, 12),
        ]

        for store, name, price, stock in products_data:
            Product.objects.update_or_create(
                store=store,
                name=name,
                defaults={
                    "price": price,
                    "stock": stock,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "DIJIKALA test data created successfully!"
            )
        )
