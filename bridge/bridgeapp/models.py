from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """abstract base model for Thread and Response"""
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        blank = True,
        null = True,
        on_delete = models.SET_NULL
        )

    class Meta:
        abstract = True


class Category(models.Model):
    """model for bridgeapp_category table"""
    type = models.CharField(max_length=50, unique=True)

    def __str___(self):
        return self.type


class Thread(Post):
    """model for bridgeapp_thread table"""
    # many-to-many relationship with Category
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username}: {self.body}"


class Response(Post):
    """model for bridgeapp_response table"""
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return f"{self.user.username}: {self.body}"
