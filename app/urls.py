from . import views
from django.urls import path

urlpatterns = [
  path('', views.home, name='home'),
  path('login', views.login, name='login'),
  path('register', views.register, name='register'),
  path('logout', views.logout, name='logout')
]