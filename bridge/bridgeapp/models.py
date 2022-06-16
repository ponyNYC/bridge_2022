from django.db import models

class Category(models.Model):
    """model for bridgeapp_category table"""
    type = models.CharField(max_length=50, unique=True)


class Thread(models.Model):
    """model for bridgeapp_thread table"""
    body = models.TextField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    # create many-to-many relationship with Category
    categories = models.ManyToManyField(Category)


class Response(models.Model):
    """model for bridgeapp_response table"""
    body = models.TextField(unique=True)
    # Thread has one-to-many responses that get deleted with it
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
