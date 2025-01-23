# # # # from django.contrib import admin
# # # # from .models import User

# # # # @admin.register(User)
# # # # class UserAdmin(admin.ModelAdmin):
# # # #     list_display = ('email', 'full_name', 'is_staff', 'is_active')
# # # #     search_fields = ('email', 'full_name')
# # # #     ordering = ('email',)


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('email', 'full_name', 'is_staff', 'is_active')
#     search_fields = ('email', 'full_name')
#     ordering = ('email',)

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('full_name', 'address', 'phone_number')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'full_name', 'address', 'phone_number', 'is_staff', 'is_active')}
#         ),
#     )

# # from django.contrib import admin
# # from django.contrib.auth.admin import UserAdmin
# # from .models import User

# # @admin.register(User)
# # class CustomUserAdmin(UserAdmin):
# #     model = User
# #     list_display = ('email', 'full_name', 'is_staff', 'is_active')
# #     search_fields = ('email', 'full_name')
# #     ordering = ('email',)

# #     fieldsets = (
# #         (None, {'fields': ('email', 'password')}),
# #         ('Personal Info', {'fields': ('full_name', 'address', 'phone_number')}),
# #         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
# #     )

# #     add_fieldsets = (
# #         (None, {
# #             'classes': ('wide',),
# #             'fields': ('email', 'password1', 'password2', 'full_name', 'address', 'phone_number', 'is_staff', 'is_active')}
# #         ),
# #     )


from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ['email', 'full_name', 'is_active', 'is_staff', 'is_superuser',]
    search_fields = ['email', 'full_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']

    # Add the option to delete users in the admin interface
    actions = ['delete_selected']

admin.site.register(User, UserAdmin)

