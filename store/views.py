
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Product, Storage1, Order
from django.contrib import messages
# from django.urls import reverse
from django.http import HttpResponse
import logging

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                address=address,
                phone_number=phone_number
            )
            user.save()
            return redirect('login')
        except Exception as e:
            return render(request, 'register.html', {'error': str(e)})
        


    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            return redirect('user')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return render(request, 'home.html',{})

@login_required
def user_view(request):
    # name = User.objects.get()
    user = request.user
    return render(request, 'user.html', {'user':user})
@login_required
def user_view(request):
    users = User.objects.all()
    products = Product.objects.all()
    return render(request, 'user.html', {'users': users, 'products': products})

# product 

def product_list(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required
def delete_user(request, user_id):
 
    if request.method == "POST":
        action = request.POST.get('action')
        # Fetch the user to be deleted
        user_to_delete = get_object_or_404(User, pk=user_id)
        if action=='del_user':
       
            if not user_to_delete.is_superuser:
                #  delete operation
                user_to_delete.delete()
                messages.success(request, f"Account: {user_to_delete.full_name} deleted successfully.")
            else:
            
                messages.error(request, "Cannot delete a superuser.")
    else:
 
        messages.error(request, "Invalid request method.")

    return redirect('user')  

# add_products 
@login_required
def add_product(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add products.")
        return redirect('home')
    

    if request.method == "POST":
        action = request.POST.get('action')
        if action=='add_prod':
            name = request.POST.get('name')
            details = request.POST.get('details')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            image = request.FILES.get('image')  
            if not name or not price or not quantity:
                messages.error(request, "Name, Price, and Quantity are required fields.")
                return redirect('user')  
            
            try:
                product = Product.objects.create(
                    name=name,
                    details=details,
                    price=price,
                    quantity=quantity,
                    image=image,
                )
                product.save()
                messages.success(request, f"Product '{product.name}' added successfully.")
            except Exception as e:
                messages.error(request, f"Error adding product: {str(e)}")
    
    return redirect('user')

def delete_product(request,product_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        product_to_delete = get_object_or_404(Product, pk=product_id)
        if action=='del_prod':
            product_to_delete.delete()
            messages.success(request, f"Product '{product_to_delete.name}' deleted successfully.")
            return redirect('user')
    return redirect('user')

@login_required
def save_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if not quantity or int(quantity) <= 0:
            messages.error(request, 'Should Keep Atleast One Product')
            return redirect('home')
        
        quantity = int(quantity)
        new_price = quantity*product.price

        storage_entry, created = Storage1.objects.get_or_create(
                user = request.user,
                product = product,
                defaults={'quantity': quantity, 'new_price': new_price}
        )

        if not created:
            storage_entry.quantity = quantity
            storage_entry.new_price = new_price
            storage_entry.save()

        messages.success(request, f"Product '{product.name}' saved successfully.")
    return redirect('cart')


@login_required
def saved_products(request):
    saved_items = Storage1.objects.filter(user=request.user) 
    return render(request, 'cart.html', {'saved_items': saved_items})

@login_required
def delete_saved_product(request, item_id):
    item = get_object_or_404(Storage1, id=item_id, user=request.user) 
    item.delete()
    messages.success(request, "Item deleted successfully.")
    return redirect('cart')

@login_required
def buy_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Storage1, id=item_id, user=request.user)
        action = request.POST.get('action')
        if action=='keep-item':
        # Create a new order
            order = Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.new_price
            )
            order.save()
         
            item.delete()

            messages.success(request, f"Order placed successfully for {order.product.name}.")
            return redirect('cart')



def orders(request, user_id):
    user = get_object_or_404(User, id=user_id)
    saved_orders = Order.objects.filter(user=user) 
    return render(request, 'order.html', {'user': user, 'orders': saved_orders})

@login_required
def user_orders(request, user_id):
    user = get_object_or_404(User, id=user_id)
    saved_orders = Order.objects.filter(user=request.user) 
    return redirect(request, 'user.html', {'user': user, 'orders': saved_orders})





def see_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'details.html', {'product':product})



# @login_required
# def see_orders(request, user_id):
#     user = get_object_or_404(User, id=user_id)  # Get the user
#     orders = Order.objects.filter(user=user)  # Fetch only this user's orders

#     if request.method == "POST":
#         order_id = request.POST.get("order_id")
#         action = request.POST.get("action")

#         if action == "pay_order":
#             order = Order.objects.get(id=order_id, user=user)  
#             order.status = "Paid"
#             order.save()

#     return render(request, "order.html", {"orders": orders})

@login_required
def see_orders(request, user_id=None):
    """Show orders based on user type"""
    if request.user.is_superuser:
        orders = Order.objects.all()  # Admin sees all orders
    else:
        orders = Order.objects.filter(user=request.user)  # User sees only their orders
    
    return render(request, "order.html", {"orders": orders})


@login_required
def pay_order(request, order_id):
    """Mark order as 'paid'"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        order.status = "paid"
        order.save()
        messages.success(request, f"Order {order.id} marked as 'Paid'.")

    return redirect('order', {"orders": orders})


@user_passes_test(lambda u: u.is_superuser)
def admin_orders(request):
    orders = Order.objects.all()
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        action = request.POST.get("action")
        order = get_object_or_404(Order, id=order_id)

        if action == "confirm_order":
            order.status = "Confirmed"
            
        elif action == "cancel_order":
            order.status = "Cancelled"
        order.save()
        messages.success(request, f"Order {order_id} updated successfully.")

    return render(request, "order.html", {"orders": orders})

@user_passes_test(lambda u: u.is_superuser)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id,)
    if request.method == 'POST':
        
        action = request.POST.get('action')
        if action=='delete_order':
      
           
            order.delete()
        
            messages.success(request, f"Order {order_id} deleted successfully.")
    return redirect('admin_orders') 