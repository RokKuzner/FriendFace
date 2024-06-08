import json
from channels.generic.websocket import AsyncWebsocketConsumer
import database as db

class DmMessagesConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    dm_id = self.scope['url_route']['kwargs']['dm_id']
    current_user_username = self.scope["session"]["current_user"]
    current_user_id = db.get_users_id_by_username(current_user_username)

    if db.dm_exists_by_id(dm_id) == False or current_user_id not in db.get_dm_members(dm_id):
      await self.close()
    else:
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

    await self.send(text_data=json.dumps({
      "staus": "connected",
      "messages": db.get_dm_messages(dm_id)
    }))