from django.contrib import admin
from .models import User, Product, Storage1, Order, DoneOrder

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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'price', 'status', 'order_date']
    list_filter = ['status', 'order_date']
    search_fields = ['user__full_name', 'product__name']
    ordering = ('-order_date',)
    list_editable = ('status',)  


@admin.register(DoneOrder)
class DoneOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_name', 'quantity', 'price', 'order_date']
    list_filter = ['order_date']
    search_fields = ['user__full_name', 'order_name']
    ordering = ('-order_date',)
