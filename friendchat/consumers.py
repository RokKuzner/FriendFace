import json
from channels.generic.websocket import WebsocketConsumer

class DmConsumer(WebsocketConsumer):
  def connect(self):
    self.accept()

    self.send(text_data=json.dumps({
      "staus": "success",
      "message": "succesfully connected"
    }))