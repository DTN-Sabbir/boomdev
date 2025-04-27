from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.user_manager.custom_user_manager import CustomUserManager


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        MANAGER = "MANAGER", _("Manager")
        USER = "USER", _("User")

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):

        return self.email

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_manager(self):
        return self.role == self.Roles.MANAGER

    @property
    def is_user(self):
        return self.role == self.Roles.USER


import uuid


class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="rest_codes"
    )
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


def is_expired(self):
    return timezone.now() > self.expires_at
