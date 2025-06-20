# notifications/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        print("user is ", user)
        
        if user and user.is_authenticated:
            self.group_name = f"user_{user.id}_notifications"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user and user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send_json(event["content"])
