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
  path('comment', views.comment, name='comment'),
  path('user/<str:user_page>', views.user, name='user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)