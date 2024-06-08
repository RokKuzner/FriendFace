from django.urls import path
from . import consumers

websochet_urlpatterns = [
  path("ws/dm-messages/<str:dm_id>", consumers.DmMessagesConsumer.as_asgi()),
  path("ws/dm-typing/<str:dm_id>", consumers.DmTyping.as_asgi())
]