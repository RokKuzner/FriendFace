from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.home, name='home'),
  path('login', views.login, name='login'),
  path('register', views.register, name='register'),
  path('logout', views.logout, name='logout'),
  path('post', views.post, name='post'),
  path('like', views.like, name='like'),
  path('apilike', views.apilike, name='api like'),
  path('comment', views.comment, name='comment'),
  path('apicomment', views.api_comment, name='api comment'),
  path('user/<str:user_page>', views.user, name='user'),
  path('follow/<str:user>', views.follow, name='follow'),
  path('unfollow/<str:user>', views.unfollow, name='unfollow'),
  path('user/<str:user>/edit', views.editprofile, name='editprofile'),
  path('getpost/<str:post_id>', views.getpost, name='editprofile'),
  path('readpost', views.readpost, name='readpost'),
  path('userexists', views.userexists, name='userexists')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)