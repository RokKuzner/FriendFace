from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('readpost', views.readpost, name='readpost'),
  path('like', views.like, name='like'),
  path('comment', views.comment, name='comment'),
  path('userexists', views.userexists, name='userexists'),
]