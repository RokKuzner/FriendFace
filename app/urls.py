from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.home, name='home'),
  path('login', views.login, name='login'),
  path('register', views.register, name='register'),
  path('logout', views.logout, name='logout'),
  path('like', views.like, name='like'),
  path('comment', views.comment, name='comment'),
  path('user/<str:user_page>', views.user, name='user'),
  path('follow/<str:user>', views.follow, name='follow'),
  path('unfollow/<str:user>', views.unfollow, name='unfollow'),
  path('user/<str:user>/edit', views.editprofile, name='editprofile'),
  path('getpost/<str:post_id>', views.getpost, name='editprofile'),
  path('search', views.search, name='search'),
]