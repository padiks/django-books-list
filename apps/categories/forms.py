# apps/categories/forms.py
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
