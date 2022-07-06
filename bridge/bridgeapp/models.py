from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Abstract base model for Thread and Response"""
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # assign primary key from built in User model
    user = models.ForeignKey(
        User,
        blank = True,
        null = True,
        on_delete = models.SET_NULL
        )

    class Meta:
        abstract = True


class Category(models.Model):
    """Model for bridgeapp_category table"""
    type = models.CharField(max_length=50, unique=True)

    def __str___(self):
        return self.type


class Thread(Post):
    """Model for bridgeapp_thread table"""
    # many-to-many relationship with Category
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username}: {self.body}"


class Response(Post):
    """Model for bridgeapp_response table"""
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return f"{self.user.username}: {self.body}"
