from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=120, unique=True)
    slug = models.SlugField(_("Slug"), max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name=_("Author")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
        verbose_name=_("Category")
    )
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=300, unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    ingredients = models.TextField(_("Ingredients"), blank=True)
    instructions = models.TextField(_("Instructions"), blank=True)
    image = models.ImageField(
        _("Image"),
        upload_to="recipes/%Y/%m/%d/",
        null=True,
        blank=True
    )
    is_draft = models.BooleanField(_("Is Draft"), default=False)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("User")
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Recipe")
    )
    text = models.TextField(_("Text"))
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.user} on {self.recipe}"


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("User")
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("Recipe")
    )
    score = models.PositiveSmallIntegerField(_("Score"))  # 1..5 validation will be in serializer
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = ("user", "recipe")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.score} by {self.user} for {self.recipe}"
