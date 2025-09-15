from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Recipe
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Recipe)
def ensure_slug_for_recipe(sender, instance, created, **kwargs):
    if not instance.slug:
        base = slugify(instance.title)[:200]
        slug = base
        # ensure unique
        i = 1
        while sender.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        instance.slug = slug
        instance.save(update_fields=["slug"])

@receiver(post_delete, sender=Recipe)
def delete_recipe_image(sender, instance, **kwargs):
    try:
        if instance.image:
            instance.image.delete(save=False)
    except Exception as e:
        logger.exception("Error deleting recipe image: %s", e)