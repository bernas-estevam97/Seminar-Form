from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .forms import SeminarForm
from .models import SeminarFormModel


@login_required(login_url=settings.LOGIN_URL)
def home_page(request):
     return render(request@login_required(login_url=settings.LOGIN_URL), 'index.html', {'form': form})

@login_required(login_url=settings.LOGIN_URL)
def seminar_form_req(request):
     if request.method=='POST':
          form = SeminarForm(request.POST)
          if form.is_valid():
               title = form.cleaned_data['seminar_title']
               speaker = form.cleaned_data['seminar_speaker']
               date = form.cleaned_data['seminar_date']
               form.save()
               return HttpResponse('Seminar form saved')
     else:
          form = SeminarForm()
# EXECEPTIONS

def error_403(request, exception):
     return render(request, 'accounts/blocked.html')


def error_404(request, exception):
     return render(request, 'accounts/not-found.html')

def error_500(request):
     return render(request, '500.html', status=500)
