from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import PermissionDenied
from .forms import LoginForm, RegisterForm  # Import your custom forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def auth_view(request):
    # Default toggle state (this will be passed to the template for toggling)
    toggle = request.GET.get('toggle', 'login')

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # Authenticate the user and log them in
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to a protected page after login
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'signup' in request.POST:
            signup_form = RegisterForm(request.POST)
            if signup_form.is_valid():
                # Save the new user
                full_name = signup_form.cleaned_data['full_name']
                username = signup_form.cleaned_data['username']
                password = signup_form.cleaned_data['password']

                user = User.objects.create_user(username=username, password=password)
                user.first_name = full_name  # Save the full name
                user.save()

                # Log the user in
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')  # Redirect to a protected page after signup
            else:
                messages.error(request, 'Please correct the errors below.')

    else:
        if toggle == 'login':
            login_form = LoginForm()
            signup_form = RegisterForm()
        else:
            signup_form = RegisterForm()
            login_form = LoginForm()

    return render(request, 'accounts/login.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'toggle': toggle
    })

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








