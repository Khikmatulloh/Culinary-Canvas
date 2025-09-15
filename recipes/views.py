from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, filters
from drf_spectacular.utils import extend_schema
from .models import Category, Recipe, Comment, Rating
from .serializers import CategorySerializer, RecipeSerializer, CommentSerializer, RatingSerializer
import logging

logger = logging.getLogger(__name__)


# ----------- Categories Views -----------

@extend_schema(tags=["Categories"])
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=["Categories"])
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"


@extend_schema(tags=["Categories"])
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=["Categories"])
class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"


@extend_schema(tags=["Categories"])
class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"


# ----------- Recipes Views -----------

@extend_schema(tags=["Recipes"])
class RecipeListView(ListAPIView):
    queryset = Recipe.objects.select_related("author", "category").all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("title", "description", "ingredients", "instructions")
    ordering_fields = ("created_at", "updated_at")


@extend_schema(tags=["Recipes"])
class RecipeDetailView(RetrieveAPIView):
    queryset = Recipe.objects.select_related("author", "category").all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Recipes"])
class RecipeCreateView(CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(
            "New recipe created by %s: %s",
            self.request.user.email,
            serializer.instance.title
        )


@extend_schema(tags=["Recipes"])
class RecipeUpdateView(UpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            logger.warning(
                "User %s tried to edit recipe %s owned by %s",
                request.user.email,
                obj.id,
                obj.author.email,
            )
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


@extend_schema(tags=["Recipes"])
class RecipeDeleteView(DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ----------- Comments Views -----------

@extend_schema(tags=["Comments"])
class CommentListView(ListAPIView):
    queryset = Comment.objects.select_related("user", "recipe").all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Comments"])
class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.select_related("user", "recipe").all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Comments"])
class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Comments"])
class CommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Comments"])
class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ----------- Ratings Views -----------

@extend_schema(tags=["Ratings"])
class RatingListView(ListAPIView):
    queryset = Rating.objects.select_related("user", "recipe").all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Ratings"])
class RatingDetailView(RetrieveAPIView):
    queryset = Rating.objects.select_related("user", "recipe").all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Ratings"])
class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.warning("Rating create error: %s", str(e))
            return Response(
                {"detail": "You may have already rated this recipe."},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=["Ratings"])
class RatingUpdateView(UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Ratings"])
class RatingDeleteView(DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
