from django.contrib import admin
from .models import Category, Thread, Response


class ThreadAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Author', {'fields': ['user']}),
        ('Question', {'fields': ['body', 'categories']}),
    ]


class ResponseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['thread']}),
        ('Response', {'fields': ['user', 'body']})
    ]



# register 3 models
admin.site.register(Category)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Response, ResponseAdmin)
