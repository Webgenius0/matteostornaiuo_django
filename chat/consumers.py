import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatRoom

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print("[DEBUG] Connected user:", self.user)

        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        try:
            self.other_user_id = int(self.scope["url_route"]["kwargs"]["user_id"])
        except (KeyError, ValueError):
            print("[DEBUG] Invalid user_id")
            await self.close()
            return

        # Deterministic room name for user pair (sorted so A-B and B-A are same)
        self.room_group_name = self.get_room_group_name(self.user.id, self.other_user_id)
        print("[DEBUG] Room group:", self.room_group_name)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()
            if not message:
                return

            # Save message and broadcast
            saved_msg = await self.save_message(self.user.id, self.other_user_id, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": saved_msg["content"],
                    "sender": saved_msg["sender"],
                    "timestamp": saved_msg["timestamp"],
                }
            )
        except Exception as e:
            print("[DEBUG] receive error:", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))

    def get_room_group_name(self, user1_id, user2_id):
        ids = sorted([user1_id, user2_id])
        return f"chat_room_{ids[0]}_{ids[1]}"

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        # Ensure same room always exists
        user_ids = sorted([sender_id, receiver_id])
        room, _ = ChatRoom.objects.get_or_create_by_users(user_ids[0], user_ids[1])

        msg = ChatMessage.objects.create(
            room=room,
            sender_id=sender_id,
            content=content,
        )

        return {
            "content": msg.content,
            "sender": msg.sender.id,
            "timestamp": str(msg.timestamp),
        }
