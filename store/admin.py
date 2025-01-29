from django.contrib import admin
from .models import User, Product, Storage1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity']

@admin.register(Storage1)
class Storage1Admin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'new_price']
    search_fields = ['user__ful_name', 'product__name']
    list_filter = ['user']