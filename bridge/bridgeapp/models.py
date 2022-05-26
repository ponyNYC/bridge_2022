from django.db import models


class Category(models.Model):
    """Category table"""
    type = models.CharField(max_length=50, unique=True)


class Thread(models.Model):
    """Thread table, includes ManyToMany fields for Categories"""
    body = models.TextField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)


class Response(models.Model):
    """Responses to Threads table, includes ForeignKey to map Many to One for Threads"""
    body = models.TextField(unique=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
