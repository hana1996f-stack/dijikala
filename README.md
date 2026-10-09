# DigiKala Project

## About the Project

This is a simple online shopping website made with Django and Python.

Customers can see products, add them to their cart, and place orders. Sellers can create their stores and manage their products.

## Technologies

* Python
* Django
* PostgreSQL
* HTML and CSS
* Git and GitHub

## Project Apps

* **accounts:** Handles user registration, login, and user profiles.
* **store:** Handles stores and products.
* **cart:** Handles the shopping cart.
* **orders:** Handles customer orders.

## Team Members

### Maedeh

My responsibilities are:

* Creating the shopping cart.
* Adding and removing products from the cart.
* Updating product quantities.
* Creating orders and showing order history.
* Implementing demo payments and updating customer and seller balances.
* Adding product search and categories.
* Adding product images.
* Checking product stock before checkout.
* Creating an order confirmation page.

### Hana

Her responsibilities are:

* Creating user registration and login.
* Creating customer and seller profiles.
* Creating and managing stores.
* Adding, editing, and showing products.
* Managing user permissions.

We will work together on connecting our apps, testing the project, and fixing errors.

## Things I Learned

### 1. `__init__.py` and Django Settings

I learned how `__init__.py` works in Python packages and how it can be used with Django settings.

I also learned how to organize settings into separate files, such as development and production settings.

### 2. `UniqueConstraint`

I learned how to use `UniqueConstraint` in the `CartItem` model.

It prevents the same customer from having multiple cart records for the same product.

If the customer adds the same product again, the application should increase the quantity of the existing item instead of creating a new one.

## Extra Features

I will also try to add some extra features, such as product search, categories, product images, stock checking, and an order confirmation page.


