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


### 2. `UniqueConstraint`

I learned how to use `UniqueConstraint` in the `CartItem` model.
It prevents the same customer from having multiple cart records for the same product.
If the customer adds the same product again, the application should increase the quantity of the existing item instead of creating a new one.

### 3. `Query Optimization`
Used `select_related("product", "product__store")` to fetch related product and store data in a single SQL query using JOINs, reducing unnecessary database queries when displaying cart items.

### 4. @require_POST
Used @require_POST to ensure that adding or removing cart items is performed only through POST requests.

### 5. `transaction.atomic()` and `with`

I learned how to use `with transaction.atomic()` in Django to manage database transactions.
It ensures that database changes within a transaction are committed if all operations succeed. If an error occurs and the transaction is rolled back, the changes made within that transaction are undone.
This is useful in the checkout process because creating an order, updating the customer's balance, and reducing product stock should work together as a single transaction.

### 6. `select_for_update()`

I learned how to use `select_for_update()` in Django to lock database rows during a transaction.
It prevents concurrent transactions from modifying the same selected rows until the current transaction finishes. This is useful during checkout because it helps prevent multiple customers from purchasing the same product based on outdated stock information.
It should be used inside `transaction.atomic()` and supported by the database backend.


## Extra Features

I will also try to add some extra features, such as product search, categories, product images, stock checking, and an order confirmation page.


