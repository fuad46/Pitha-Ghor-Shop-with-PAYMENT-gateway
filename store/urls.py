from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('user/', views.user_view, name='user'),
  path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
  path('product/add/', views.add_product, name='add_product'),
  path('product/<int:product_id>/delete', views.delete_product, name='delete_product'),
  path('save_product/<int:product_id>/', views.save_product, name='save_product'),
  path('cart/', views.saved_products, name='cart'),
]