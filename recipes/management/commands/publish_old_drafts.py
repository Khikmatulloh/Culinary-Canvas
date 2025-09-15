# recipes/management/commands/publish_old_drafts.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.apps import apps
import logging

logger = logging.getLogger("recipes")


class Command(BaseCommand):
    help = "Publish old drafts: set is_draft=False for recipes older than --days (default 30)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Number of days; drafts older than this will be published.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed but do not commit.",
        )

    def handle(self, *args, **options):
        Recipe = apps.get_model("recipes", "Recipe")
        days = options["days"]
        dry_run = options["dry_run"]
        cutoff = timezone.now() - timedelta(days=days)
        qs = Recipe.objects.filter(is_draft=True, created_at__lt=cutoff)
        count = qs.count()
        self.stdout.write(f"Found {count} draft(s) older than {days} days.")
        if count == 0:
            return

        if dry_run:
            for r in qs:
                self.stdout.write(f"DRY RUN: would publish Recipe(id={r.pk}, title={getattr(r, 'title', '')})")
            return

        updated = qs.update(is_draft=False)
        self.stdout.write(self.style.SUCCESS(f"Published {updated} recipe(s)."))
        logger.info("Published %s old draft(s) older than %s days", updated, days)