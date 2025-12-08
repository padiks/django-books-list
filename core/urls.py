from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage → books module
    path('', include('apps.books.urls')),
	path('categories/', include('apps.categories.urls')),
]
