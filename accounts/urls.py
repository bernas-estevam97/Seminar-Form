from django.urls import path
from . import views


urlpatterns = [
    path('account-auth/', views.auth_view, name="auth"),
    #path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('banned/', views.banned_user_view, name='banned_user'),
]