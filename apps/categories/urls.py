# apps/categories/urls.py
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
