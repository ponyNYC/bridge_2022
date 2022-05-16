from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.
class Category(models.Model):
    type=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255, null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.type)
        super(Category, self).save(*args, **kwargs)
class Thread(models.Model):
    # post_id=models.AutoField(primary_key=True)
    body=models.TextField(blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    categories=models.ManyToManyField(Category)

class Response(models.Model):
    body=models.TextField(blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    