from django.contrib import admin
from .models import Category, Thread, Response

# register 3 models
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Response)
