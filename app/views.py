from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages



def index(request):
    return render(request, 'index.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username is already taken')

        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.info(request,'Account Create successfully')
            return redirect('home')  
        else:
            # Handle password mismatch error
            messages.info(request,'Password do not match')
            return render(request, 'signup.html')
    
        
    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
        else:
            # If no "@", treat it as a username
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'successful login')
            return redirect('home')
        else:
            # Handle invalid login
            messages.error(request, 'Invalid username/email or password')
            return redirect('login')

    return render(request, 'login.html')
    

def user_logout(request):
    logout(request)
    return redirect('login')

