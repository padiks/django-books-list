# apps/books/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden  # Returns 403 Forbidden when user lacks permission
from .models import Books
from .forms import BooksForm


def index(request):
    records = Books.objects.select_related('category').order_by('id')
    return render(request, 'books/index.html', {
        'title': 'Books List',
        'books': records,
    })


def view_record(request, pk):
    book = get_object_or_404(Books, pk=pk)
    return render(request, 'books/view.html', {
        'title': f'View Book: {book.title}',
        'book': book,
    })


def add_record(request):
    if request.method == 'POST':
        form = BooksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:index')
    else:
        form = BooksForm()

    return render(request, 'books/form.html', {
        'title': 'Add Book',
        'form': form,
    })


def edit_record(request, pk):
    book = get_object_or_404(Books, pk=pk)

    if request.method == 'POST':
        form = BooksForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:index')
    else:
        form = BooksForm(instance=book)

    return render(request, 'books/form.html', {
        'title': f'Edit Book: {book.title}',
        'form': form,
    })


# def delete_record(request, pk):
#    book = get_object_or_404(Books, pk=pk)
#    book.delete()
#    return redirect('books:index')

def delete_record(request, pk):
    # Only allow logged-in superusers (Admin)
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this book.")

    book = get_object_or_404(Books, pk=pk)
    book.delete()
    return redirect('books:index')
