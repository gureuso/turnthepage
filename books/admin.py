from django.contrib import admin

from .models import Book, Page, Category

admin.site.register(Book)
admin.site.register(Page)
admin.site.register(Category)
