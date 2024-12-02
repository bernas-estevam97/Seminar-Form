from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_page(request):
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


def login_page(request):
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, ('You have logged out. Log in again to access the app.'))
    return redirect('/')








