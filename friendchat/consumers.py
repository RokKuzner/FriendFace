import json
from channels.generic.websocket import AsyncWebsocketConsumer
import database as db
import FriendChatTyping as fct

class DmMessagesConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    dm_id = self.scope['url_route']['kwargs']['dm_id']
    current_user_username = self.scope["session"]["current_user"]
    current_user_id = db.get_users_id_by_username(current_user_username)

    if db.dm_exists_by_id(dm_id) == False or current_user_id not in db.get_dm_members(dm_id):
      await self.close()
      return

    self.room_group_name = f"messages_{dm_id}"
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )
  
    await self.accept()

    await self.send(text_data=json.dumps({
      "staus": "connected",
      "messages": db.get_dm_messages(dm_id)
    }))

  async def receive(self, text_data):
    dm_id = self.scope['url_route']['kwargs']['dm_id']
    current_user_username = self.scope["session"]["current_user"]
    current_user_id = db.get_users_id_by_username(current_user_username)
  
    text_data_json = json.loads(text_data)
    message_content = text_data_json["message"]

    db.new_message(dm_id, current_user_id, message_content)

    await self.channel_layer.group_send(
      self.room_group_name, {"type": "chat_message"}
    )    

  async def chat_message(self, event):
    dm_id = self.scope['url_route']['kwargs']['dm_id']

    await self.send(text_data=json.dumps({
      "staus": "connected",
      "messages": db.get_dm_messages(dm_id)
    }))

class DmTyping(AsyncWebsocketConsumer):
  async def connect(self):
    dm_id = self.scope['url_route']['kwargs']['dm_id']
    current_user_username = self.scope["session"]["current_user"]
    current_user_id = db.get_users_id_by_username(current_user_username)

    if db.dm_exists_by_id(dm_id) == False or current_user_id not in db.get_dm_members(dm_id):
      await self.close()
      return

    self.room_group_name = f"typers_{dm_id}"
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )
  
    await self.accept()

    await self.send(text_data=json.dumps({
      "staus": "connected",
      "users typing": fct.get_currently_typing_in_dm(dm_id)
    }))

  async def receive(self, text_data):
    dm_id = self.scope['url_route']['kwargs']['dm_id']
    current_user_username = self.scope["session"]["current_user"]
    current_user_id = db.get_users_id_by_username(current_user_username)
  
    text_data_json = json.loads(text_data)
    is_typing = text_data_json["is_typing"]

    if is_typing == "true":
      fct.start_typing(dm_id, current_user_id)
    elif is_typing == "false":
      fct.stop_typing(dm_id, current_user_id)

    await self.channel_layer.group_send(
      self.room_group_name, {"type": "chat_typing"}
    )    

  async def chat_typing(self, event):
    dm_id = self.scope['url_route']['kwargs']['dm_id']

    await self.send(text_data=json.dumps({
      "staus": "connected",
      "users typing": fct.get_currently_typing_in_dm(dm_id)
    }))

  async def disconnect(self, code):
    dm_id = self.scope['url_route']['kwargs']['dm_id']
    current_user_username = self.scope["session"]["current_user"]
    current_user_id = db.get_users_id_by_username(current_user_username)

    fct.stop_typing(dm_id, current_user_id)

    await self.channel_layer.group_send(
      self.room_group_name, {"type": "chat_typing"}
    )