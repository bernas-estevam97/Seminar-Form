from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm

def register_page(request):
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def login_user(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            ip = get_client_ip(request)
            if ip:
                key = f'failed_login_attempts_{ip}'
                cache.delete(key)
            return redirect('/')
        else:
            ip = get_client_ip(request)
            if ip:
                key = f'failed_login_attempts_{ip}'
                attempts = cache.get(key, 0)
                attempts += 1
                cache.set(key, attempts, timeout=settings.FAILED_LOGIN_LOCK_DURATION) #IPLockOutMiddleWare         
                if attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS: #IpLockOutMiddleware
                    # return render(request, 'authenticate/blocked.html', {})
                    messages.error(request, (f"You have been blocked for several failed login attempts."))
                    raise PermissionDenied()
                else:
                    messages.error(request, (f"Invalid login. {attempts} of {settings.MAX_FAILED_LOGIN_ATTEMPTS} attempts left"))
                    #cache._cache.keys() cache._cache.values()
                    # print(cache._cache.keys())
                    return render(request, 'accounts/login.html', {})
    else:
        return render(request, 'accounts/login.html', {})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def login_page(request):
#     form = UserCreationForm()
#     context = {'form':form}
#     return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, ('You have logged out. Log in again to access the app.'))
    return redirect('/')








