from django.conf import settings
from django.urls import reverse

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
