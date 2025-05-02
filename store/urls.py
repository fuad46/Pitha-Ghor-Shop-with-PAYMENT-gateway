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
  path('orders/pay/<int:order_id>/', views.pay_order, name='pay_order'),


  path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),

  path('details/<int:product_id>/', views.see_details, name='details'),
 
  path('orders/admin/', views.admin_orders, name='admin_orders'),
  path('all-products', views.all_products, name='all-products'),

# paypal
  path('orders/paypal-complete/<int:order_id>/', views.paypal_complete, name='paypal_complete'),
  path('orders/<int:user_id>/', views.see_orders, name='orders'),
  path('orders/paypal-complete/<int:order_id>/',views.paypal_complete,name='paypal_complete'),
# paypal


  path('done_order/', views.done_order, name='done_order'),
  path('done_order/<int:order_id>/delete/' , views.del_dn_orders, name='delete_dn_orders'),


  path('search/', views.search_products, name='search-products'),

  path('admin-order/', views.status_admin_order, name='status-admin-order'),
  path('see-admin/', views.see_admin, name='see-admin'),

  path('deluser/', views.seedeluser, name='deluser'),
  path('delete_user_admin/<int:user_id>/delete/', views.delete_user_admin, name='admin-deluser'),

]




