from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.conf import settings
# from django.core.exceptions import PermissionDenied
from .forms import LoginForm, RegisterForm  # Import your custom forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
from django.core.cache import cache  # Django cache system
from django.utils.timezone import now, timedelta  # For setting expiration time




# Set the maximum allowed login attempts and ban duration
MAX_FAILED_ATTEMPTS = 5  # Maximum number of allowed failed login attempts
BAN_DURATION = timedelta(minutes=1)  # Duration for the IP to be banned after max attempts

def auth_view(request):
    toggle = request.GET.get('toggle', 'login')
    next_url = request.GET.get('next', request.POST.get('next', '/'))

    ip_address = request.META.get('REMOTE_ADDR')
    failed_attempts = cache.get(f"failed_attempts_{ip_address}", 0)

    # Check for ban
    if failed_attempts >= MAX_FAILED_ATTEMPTS:
        ban_time = cache.get(f"ban_time_{ip_address}")
        if ban_time:
            remaining_time = ban_time - now()
            if remaining_time > timedelta(seconds=0):
                return redirect('banned_user')
            else:
                cache.delete(f"ban_time_{ip_address}")
                cache.delete(f"failed_attempts_{ip_address}")

    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        url = 'https://www.google.com/recaptcha/api/siteverify'
        response = requests.post(url, data=data)
        result = response.json()

        if not result.get('success'):
            messages.error(request, 'reCAPTCHA validation failed. Please try again.')
            return redirect(request.path)

        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            signup_form = RegisterForm()
            toggle = 'login'

            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)

                if user:
                    login(request, user)
                    cache.delete(f"failed_attempts_{ip_address}")
                    return redirect(next_url)
                else:
                    failed_attempts += 1
                    cache.set(f"failed_attempts_{ip_address}", failed_attempts, timeout=int(BAN_DURATION.total_seconds()))
                    if failed_attempts >= MAX_FAILED_ATTEMPTS:
                        cache.set(f"ban_time_{ip_address}", now() + BAN_DURATION, timeout=int(BAN_DURATION.total_seconds()))
                        messages.error(request, "Too many failed login attempts. Your account has been temporarily locked.")
                        return redirect('banned_user')

                    remaining_attempts = MAX_FAILED_ATTEMPTS - failed_attempts
                    messages.error(request, f'Invalid username or password. You have {remaining_attempts} attempt(s) left.')

            else:
                messages.error(request, 'Please correct the errors below.')
            return redirect(request.path)  # 🔁 redirect here always after POST

        elif 'signup' in request.POST:
            signup_form = RegisterForm(request.POST)
            login_form = LoginForm()
            toggle = 'signup'

            if signup_form.is_valid():
                first_name = signup_form.cleaned_data['first_name']
                last_name = signup_form.cleaned_data['last_name']
                username = signup_form.cleaned_data['username']
                password = signup_form.cleaned_data['password']

                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists. Please choose a different one.")
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    user = authenticate(request, username=username, password=password)
                    if user:
                        login(request, user)
                        return redirect(next_url)
                    else:
                        messages.error(request, 'Authentication failed after user creation.')
            else:
                if signup_form.errors.get('confirm_password'):
                    messages.error(request, "Passwords do not match")
                else:
                    messages.error(request, 'Something went wrong. Try again.')
            return redirect(request.path)  # 🔁 again, redirect after POST

    # GET request - show empty forms
    login_form = LoginForm()
    signup_form = RegisterForm()

    return render(request, 'accounts/login.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'toggle': toggle,
        'next': next_url
    })
         


def banned_user_view(request):
    ip_address = request.META.get('REMOTE_ADDR')
    ban_time = cache.get(f"ban_time_{ip_address}")

    if ban_time:
        remaining_time = ban_time - now()
        if remaining_time > timedelta(seconds=0):
            time_left = max(1, remaining_time.seconds // 60)  # Avoid 0 min display
            storage = messages.get_messages(request)
            list(storage)  # This actually consumes the messages and clears them
            return render(request, 'accounts/banned_user.html', {'time_left': time_left})

    # If ban expired, redirect to login
    return redirect('auth')


def logout_user(request):
    logout(request)
    messages.success(request, ('You have logged out. Log in again to access the app.'))
    return redirect('/')








