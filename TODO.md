# Task: Add Product CRUD (Create, Read, Update, Delete) for products_product table

## Information Gathered:

- models.py: Product (name, description, category FK, sku unique, barcode, unit_price, cost_price, reorder_level, image URL, is_active)
- views.py/urls.py/admin.py: Empty
- templates: None
- Goal: Non-admin CRUD for auth users (add, list catalog, edit, delete, toggle active)

## Plan:

1. products/admin.py: Register Product/Category for admin
2. products/views.py: ListView, CreateView, UpdateView, DeleteView, ToggleActiveView
3. products/urls.py: Patterns for CRUD
4. products/templates/products/: list.html, form.html, confirm_delete.html
5. Add nav link to accounts/templates/home/index.html
6. Migrate if needed

## Dependent Files:

- accounts/templates/home/index.html (nav link)

## Followup Steps:

1. python manage.py makemigrations products
2. python manage.py migrate
3. python manage.py createsuperuser (if needed)
4. Test: /products/ list → add → catalog → edit/delete/active toggle

Confirm plan before implementing?
