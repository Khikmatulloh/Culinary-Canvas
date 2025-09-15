from django.contrib import admin
from .models import Category, Recipe, Comment, Rating
from modeltranslation.admin import TranslationAdmin


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(TranslationAdmin):
    list_display = ("title", "author", "category", "is_draft", "created_at")
    list_filter = ("category", "is_draft", "created_at")
    search_fields = ("title", "author__email", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(Comment)
class CommentAdmin(TranslationAdmin):
    list_display = ("user", "recipe", "created_at")
    search_fields = ("user__email", "recipe__title", "text")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "score", "created_at")
    list_filter = ("score",)
    search_fields = ("user__email", "recipe__title")
