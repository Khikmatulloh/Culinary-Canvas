# recipes/apps.py
from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"

    def ready(self):
        try:
            import recipes.signals  
        except Exception:
            pass