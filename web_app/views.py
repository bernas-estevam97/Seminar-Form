from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url=settings.LOGIN_URL)
def home_page(request):
     return render(request, 'index.html')

# EXECEPTIONS

def error_403(request, exception):
     return render(request, 'accounts/blocked.html')


def error_404(request, exception):
     return render(request, 'accounts/not-found.html')

def error_500(request):
     return render(request, '500.html', status=500)
