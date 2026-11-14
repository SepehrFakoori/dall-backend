from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    """Custom user model"""

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
