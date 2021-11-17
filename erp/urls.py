from django.urls import path

from . import views

urlpatterns = [
    path('signin', views.index),
    path('dashboard', views.dashboard , name = 'dashboard'),
    path('register', views.register, name = 'register'),
    path('signin', views.index, name = 'signin'),    
]