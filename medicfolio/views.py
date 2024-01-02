from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from users.models import User
from django.http import HttpResponse
from .forms import RegisterForm

from products.models import Product

def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.user.is_authenticated:
       return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request,'Bienvenido {}'.format(user.username))
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no validos')
    return render(request, 'users/login.html', {

    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    form=RegisterForm(request.POST or None)

    if request.method=='POST' and form.is_valid():
        username=form.cleaned_data.get('username')
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')

        user= form.save()
        if user:
            login(request,user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')
        
    return render(request, 'users/register.html', {
        'form':form
    })