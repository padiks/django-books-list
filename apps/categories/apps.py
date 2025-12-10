# apps/categories/apps.py
from django.apps import AppConfig

# Must match with `core/settings.py`
class CategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.categories'
