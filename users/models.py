from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = None

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'
