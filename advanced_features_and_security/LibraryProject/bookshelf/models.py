from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add additional fields here if needed
    pass

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.published_date})"
