from django.shortcuts import render

def index(request):
    context = {
        'title': 'Books List',  # Dynamic page title
    }
    return render(request, 'books/index.html', context)
