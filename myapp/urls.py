from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.index, name='index'),
    path("modal_site/", views.modal_site, name='modal_site'),
    path("register/", views.register, name='register'),
    path("login/", auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout')
]