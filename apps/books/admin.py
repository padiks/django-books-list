# apps/books/admin.py
from django.contrib import admin
from .models import Books

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'published_date')
    search_fields = ('title', 'hepburn', 'author', 'release')
    list_filter = ('category', 'published_date')
