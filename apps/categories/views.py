# apps/categories/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden  # Returns 403 Forbidden when user lacks permission
from .models import Categories
from .forms import CategoriesForm


def index(request):
    records = Categories.objects.all().order_by('id')
    return render(request, 'categories/index.html', {
        'title': 'Categories List',
        'categories': records,  # matches template variable
    })


def view_record(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    return render(request, 'categories/view.html', {  # create view.html template
        'title': f'View Category: {category.name}',
        'category': category,
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

# (1)
# from django.http import HttpResponse
# def delete_record(request, pk):
#    return HttpResponse("Delete is temporarily disabled.")

# (2)
# def delete_record(request, pk):
#    category = get_object_or_404(Categories, pk=pk)
#    category.delete()
#    return redirect('categories:index')

# (3)
# Only allow logged-in Admin user to delete record
def delete_record(request, pk):
    # Only allow logged-in superusers (Admin)
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this record.")

    category = get_object_or_404(Categories, pk=pk)
    category.delete()
    return redirect('categories:index')
