
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Product, Storage1
from django.contrib import messages


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