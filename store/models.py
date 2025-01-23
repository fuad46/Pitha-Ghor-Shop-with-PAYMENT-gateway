# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         return self.create_user(email, password, **extra_fields)
    
#     # def delete(self, *args, **kwargs):
#     #     # Clear related objects explicitly before deletion
#     #     self.groups.clear()
#     #     self.user_permissions.clear()
#     #     super().delete(*args, **kwargs)


# class User(AbstractBaseUser, PermissionsMixin):  # Inherit PermissionsMixin
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
    
#     # date_joined = models.DateTimeField(auto_now_add=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['full_name', 'address', 'phone_number']

#     def __str__(self):
#         return self.email


#     # Implement has_module_perms to return if the user has any module permissions
#     def has_module_perms(self, app_label):
#         return True

#     # Implement has_perm to return if the user has a specific permission
#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # user = models.ForeignKey(User, on_delete=models.CASCADE) 
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
   
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'address', 'phone_number']

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        """
        Deletes a user and clears their related permissions.
        """
        self.groups.clear()
        self.user_permissions.clear()
        super().delete(using=using, keep_parents=keep_parents)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Cascade delete orders when the user is deleted
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
