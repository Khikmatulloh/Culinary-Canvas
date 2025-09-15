from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView,
    CommentListView, CommentDetailView, CommentCreateView, CommentUpdateView, CommentDeleteView,
    RatingListView, RatingDetailView, RatingCreateView, RatingUpdateView, RatingDeleteView,
)

urlpatterns = [
    # Categories
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/<slug:slug>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<slug:slug>/delete/", CategoryDeleteView.as_view(), name="category-delete"),

    # Recipes
    path("recipes/", RecipeListView.as_view(), name="recipe-list"),
    path("recipes/create/", RecipeCreateView.as_view(), name="recipe-create"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipes/<int:pk>/update/", RecipeUpdateView.as_view(), name="recipe-update"),
    path("recipes/<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe-delete"),

    # Comments
    path("comments/", CommentListView.as_view(), name="comment-list"),
    path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),

    # Ratings
    path("ratings/", RatingListView.as_view(), name="rating-list"),
    path("ratings/create/", RatingCreateView.as_view(), name="rating-create"),
    path("ratings/<int:pk>/", RatingDetailView.as_view(), name="rating-detail"),
    path("ratings/<int:pk>/update/", RatingUpdateView.as_view(), name="rating-update"),
    path("ratings/<int:pk>/delete/", RatingDeleteView.as_view(), name="rating-delete"),
]
