from . import views
from django.urls import path

urlpatterns = [
  path('', views.home, name='home'),
  path('dm/<str:dm_id>', views.dm, name='dm'),
  path('new', views.new_dm, name='add new dm')
]