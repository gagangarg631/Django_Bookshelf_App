from django.contrib import admin

from .models import Book,Tags

# Register your models here.

admin.site.register(Book)
admin.site.register(Tags)