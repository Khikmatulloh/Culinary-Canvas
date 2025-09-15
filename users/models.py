from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_("Email Address"), unique=True)
    first_name = models.CharField(_("First Name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=150, blank=True)
    profile_image = models.ImageField(
        _("Profile Image"),
        upload_to="profiles/%Y/%m/%d/",
        null=True,
        blank=False
    )
    is_chef = models.BooleanField(_("Is Chef"), default=False)
    telegram_id = models.CharField(
        _("Telegram ID"),
        max_length=64,
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
