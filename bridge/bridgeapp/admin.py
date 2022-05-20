from django.contrib import admin
from .models import Category, Thread, Response

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('type',)}
# Register your models here.
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Response)
