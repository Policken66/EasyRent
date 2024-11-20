from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) # Автоматический вход
            return redirect('core:home')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/') 


