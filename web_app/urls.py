"""
URL configuration for web_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from web_app.views import *


urlpatterns = [
    path('access_adm_obliviouz/', admin.site.urls),
    path('', home_page, name='home'),
    path('authenticate/', include('django.contrib.auth.urls')),
    path('authenticate/', include('accounts.urls')),
    path('add-form', seminar_form_req),
    path('form-list', all_seminars, name="full-list"),
    path('generate_report', generate_report, name="generate_report"),
    path('form-list/delete_seminar/<int:seminar_id>/', delete_seminar, name='delete_seminar'),
]+ static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)



from django.conf.urls import handler500, handler404, handler403

handler403 = 'web_app.views.error_403'
handler404 = 'web_app.views.error_404'
handler500 = 'web_app.views.error_500' 