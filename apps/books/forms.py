# apps/books/forms.py
from django import forms
from .models import Books


class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = [
            'category',
            'published_date',
            'title',
            'hepburn',
            'author',
            'release',
            'url',
            'summary',
        ]

        widgets = {
            'category': forms.Select(attrs={
                'class': 'border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'published_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full'
            }),
            'hepburn': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full'
            }),
            'author': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full'
            }),
            'release': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full'
            }),
            'url': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full'
            }),
            'summary': forms.Textarea(attrs={
                'rows': 4,
                'class': 'border rounded px-3 py-2 w-full'
            }),
        }
