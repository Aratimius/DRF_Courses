from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="телефон"
    )
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name="город")
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
