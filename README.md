## **Books List (Django + Tailwind + DataTables)**

A Django project designed to learn the basics of working with databases, implementing CRUD operations, and integrating **Tailwind CSS** for responsive and clean front-end styling. This project includes features for managing books and categories, providing a simple introduction to database management and web development with Django and Tailwind.

In addition, the project uses **DataTables** to enhance the display of data in tables, providing interactive features such as search, sorting, and pagination—making it more efficient and user-friendly when managing large datasets.

The repository includes a **sample SQLite database (`db.sqlite3`)** with preloaded tables and test data.

Available login credentials:

* **User account:** `user` / `@User123`
* **Admin account:** `admin` / `root`

## Project Structure

```plaintext
project_folder/
├── db.sqlite3                 # SQLite database
├── manage.py
├── core/
│   ├── settings.py            # Django settings
│   └── urls.py                # URL routing for the project
├── templates/
│   └── base.html              # Global base layout
│
└── static/
│   ├── css/
│   │   └── components.css     # Global Tailwind CSS
│   └── img/
│       └── favicon.png        # Global images
└── apps/
    ├── categories/            # Categories feature
    │   ├── apps.py            # App configuration
    │   ├── views.py           # View logic for categories
    │   ├── urls.py            # URL routing for categories
    │   └── templates/
    │       └── categories/
    │           ├── form.html  # Form for adding/editing categories
    │           ├── index.html # List of all categories
    │           └── view.html  # Detailed view for a category
    └── books/                 # Books feature
        ├── apps.py            # App configuration
        ├── views.py           # View logic for books
        ├── urls.py            # URL routing for books
        └── templates/
            └── books/
                └── index.html # List of books
```

## Setup

### 1. Install Dependencies

Make sure you have **Python 3** and **Django** installed. If you don't, it's recommended to set up a virtual environment to keep your dependencies isolated. Here’s how you can do it:

```bash
$ mkdir <project-folder>
$ cd <project-folder>
$ python3 -m venv venv              # Create a virtual environment
$ source venv/bin/activate          # Activate the virtual environment (Debian)
(venv) $ pip install --upgrade pip
(venv) $ pip install django         # Install Django within the virtual environment
```

This approach keeps your project's dependencies separate from the global Python environment. If you choose not to use a virtual environment, you can install Django globally, but using a virtual environment is highly recommended to avoid version conflicts.

Then install any other requirements you might have (add them to `requirements.txt` if needed).

### 2. Apply Migrations

Run the following commands to set up the database:

```bash
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
```

### 3. Create a Superuser

To access the admin panel, create a superuser:

```bash
(venv) $ python manage.py createsuperuser
```

Follow the prompts to create the superuser.

### 4. Run the Development Server

Start the server:

```bash
(venv) $ python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

### 5. Access the Admin Panel

To manage **categories** through the admin panel, visit `http://127.0.0.1:8000/admin/` and log in using the superuser credentials.

## Configuration

### `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.books',  # @added
    'apps.categories',  # @added
]
```

### `TEMPLATES`

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # @updated
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### `STATIC_URL` and `STATICFILES_DIRS`

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # @added
```

---

## Views and Code for Categories

### `apps/categories/models.py`

```python
from django.db import models

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
```

### `apps/categories/forms.py`

```python
from django import forms
from .models import Categories

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'description']  # no status field here

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter category description',
                'rows': 3
            }),
        }
```

### `apps/categories/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categories
from .forms import CategoriesForm


def index(request):
    records = Categories.objects.all().order_by('id')
    return render(request, 'categories/index.html', {
        'title': 'Categories List',
        'categories': records,  # matches template variable
    })


def add_record(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories:index')
    else:
        form = CategoriesForm()

    return render(request, 'categories/form.html', {
        'title': 'Add Category',
        'form': form,
    })


def view_record(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    return render(request, 'categories/view.html', {  # create view.html template
        'title': f'View Category: {category.name}',
        'category': category,
    })


def edit_record(request, pk):
    category = get_object_or_404(Categories, pk=pk)

    if request.method == 'POST':
        form = CategoriesForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories:index')
    else:
        form = CategoriesForm(instance=category)
        # Disable 'name' field and add Tailwind styles for disabled
        form.fields['name'].disabled = True
        form.fields['name'].widget.attrs.update({
            'class': 'bg-gray-100 cursor-not-allowed border-gray-300 rounded px-2 py-1 w-full'
        })

    return render(request, 'categories/form.html', {
        'title': f'Edit Category: {category.name}',
        'form': form,
    })


def delete_record(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    category.delete()
    return redirect('categories:index')
```

### `apps/categories/urls.py`

```python
from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_record, name='add'),
    path('view/<int:pk>/', views.view_record, name='view'),   # @added view page
    path('edit/<int:pk>/', views.edit_record, name='edit'),
    path('delete/<int:pk>/', views.delete_record, name='delete'),
]
```

---

### Templates

#### `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>{% load static %}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}{% endblock %} - Toshokan</title>
<link href="{% static 'img/favicon.png' %}" rel="icon" type="image/x-icon">
<link href="{% static 'css/components.css' %}?v=1.0.0" rel="stylesheet">
<!-- Tailwind CSS CDN -->
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-800">
<header class="bg-white shadow-sm">
  <div class="container mx-auto px-4 py-3 flex items-center">   
    <h1 class="text-xl font-semibold text-gray-800">Toshokan</h1>
    <nav class="ml-8 mt-1.5 flex gap-4 text-sm font-medium">
      <a href="{% url 'books:index' %}" class="text-gray-600 hover:text-gray-900 border-b-2 border-transparent hover:border-gray-400 transition">Books</a>
      <a href="{% url 'categories:index' %}" class="text-gray-600 hover:text-gray-900 border-b-2 border-transparent hover:border-gray-400 transition">Categories</a>
      <a href="{% url 'admin:index' %}" class="text-gray-600 hover:text-gray-900 border-b-2 border-transparent hover:border-gray-400 transition">Admin</a>
    </nav>
  </div>
</header>
<main class="container mx-auto px-4 my-6">
  {% block content %}{% endblock %}
</main>
<footer></footer>
<!-- Optional: jQuery + DataTables JS for interactivity -->
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<script>
$(document).ready(function () {
  $('#itemsTable').DataTable({
    "pageLength": 10,
    "lengthMenu": [5, 10, 20, 50],
  });
});
</script>
</body>
</html>
```

---

### SQLite

```
$ python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='user')
>>> user.set_password('@User123')
>>> user.save()
>>> exit()
```

> This snippet demonstrates how to set or reset a user’s password in Django via the shell. It retrieves an existing user by username, updates their password securely using Django’s hashing mechanism, and saves the changes so the user can log in with the new password.

---

### Notes:

* **Categories**: Categories management with add, edit, view, and delete functionality.
* **Tailwind Styling**: Clean, responsive layout utilizing Tailwind CSS.
* **Django Admin**: Admin interface for managing categories through Django's built-in admin panel.
* **Modular Structure**: The project is structured in a modular and scalable way. If you need to add another module (e.g., Books), you can simply copy the `categories` folder, adjust the necessary files, and adapt it according to your new module.
* **Templates**: Other templates (e.g., for Categories & Books) can be viewed once the project is downloaded and set up locally.

---

### ⚠️ Disclaimer / Additional Note

This project demonstrates a **basic Django CRUD (Create, Read, Update, Delete) implementation** intended as a **starting reference** for building database-driven applications or for learning how to structure a clean Django project.

It focuses on:

* Clear and minimal CRUD patterns
* Proper app modularization
* Simple, readable code suitable for beginners

This project **does not include advanced features** such as:

* User authentication or login systems
* Role-based or permission-based access control
* API endpoints
* Advanced security or production-level configurations

If you require authentication, authorization, or a more complete system setup, you can refer to my other project here:
👉 [https://github.com/padiks/django-modular-project](https://github.com/padiks/django-modular-project)

That repository builds on the same modular principles while introducing more advanced Django features.

---

## 📄 License

This project is for **learning and educational use**.
Feel free to explore, extend, and build upon it.
