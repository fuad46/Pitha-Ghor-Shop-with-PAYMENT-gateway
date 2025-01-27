
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Product
from django.contrib import messages


def home(request):
    return render(request, 'home.html', {})

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
    return render(request, 'home.html')

@login_required
def user_view(request):
    # name = User.objects.get()
    user = request.user
    return render(request, 'user.html', {'user':user})
@login_required
def user_view(request):
    users = User.objects.all()
    return render(request, 'user.html', {'users': users})

# product 

def product_list(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})



@login_required
def delete_user(request, user_id):
    """
    Deletes a user if the logged-in user has the appropriate permissions.
    Superusers cannot be deleted via this function.
    """
    if request.method == "POST":
        # Fetch the user to be deleted or return a 404 if not found
        user_to_delete = get_object_or_404(User, pk=user_id)

        # Check if the user is a superuser
        if not user_to_delete.is_superuser:
            # Perform the delete operation
            user_to_delete.delete()
            messages.success(request, f"User {user_to_delete.full_name} deleted successfully.")
        else:
            # Prevent deletion of superusers
            messages.error(request, "Cannot delete a superuser.")
    else:
        # If the request is not POST, redirect to the home page
        messages.error(request, "Invalid request method.")

    return redirect('user')  # Replace 'home' with your actual homepage U