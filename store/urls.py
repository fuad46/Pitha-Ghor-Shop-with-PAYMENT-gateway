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
  path("delete-saved/<int:item_id>/cart", views.delete_saved_product, name="delete_saved_product"),
  path('cart/', views.saved_products, name='cart'),
  path('buy-item/<int:item_id>/', views.buy_item, name='buy_item'),


  path('cart/<int:product_id>/', views.user_orders, name='user_orders'),



  path('order/', views.see_orders, name='see_orders'),

  path('orders/<int:user_id>/', views.see_orders, name='orders'),
  path('orders/admin/', views.admin_orders, name='admin_orders'),
  path('orders/<int:order_id>/pay/', views.pay_order, name='pay_order'),
  path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),

  path('details/<int:product_id>/', views.see_details, name='details'),

]