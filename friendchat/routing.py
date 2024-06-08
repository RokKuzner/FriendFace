from django.urls import re_path
from . import consumers

websochet_urlpatterns = [
  re_path(r"ws/socket-server/", consumers.DmConsumer.as_asgi())
]