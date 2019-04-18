from django.contrib import admin

from .models import Book, Page, Category, AdminCoupon, Coupon

admin.site.register(Book)
admin.site.register(Page)
admin.site.register(Category)
admin.site.register(AdminCoupon)
admin.site.register(Coupon)
