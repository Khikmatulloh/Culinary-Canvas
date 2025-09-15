from rest_framework import serializers
from .models import Category, Recipe, Comment, Rating
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
        read_only_fields = ("id", "slug")

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ("id","title","slug","description","ingredients","instructions","image","is_draft","category","author","created_at","updated_at")
        read_only_fields = ("id","slug","author","created_at","updated_at")

    def get_author(self, obj):
        return {"id": obj.author.id, "email": getattr(obj.author, "email", None)}

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id","user","recipe","text","created_at")
        read_only_fields = ("id","user","created_at")

    def get_user(self, obj):
        return {"id": obj.user.id, "email": getattr(obj.user, "email", None)}

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = ("id","user","recipe","score","created_at")
        read_only_fields = ("id","user","created_at")

    def get_user(self, obj):
        return {"id": obj.user.id, "email": getattr(obj.user, "email", None)}

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)