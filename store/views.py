from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User

# Create your views here.
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
                phone_number=phone_number)
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
      return redirect('home')
    else:
       return render(request, 'login.html', {'error': 'Invalid email or password'})
  
  return render(request, 'login.html')