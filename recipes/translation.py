from modeltranslation.translator import register, TranslationOptions
from .models import Category, Recipe, Comment

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'ingredients', 'instructions')

@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('text',)