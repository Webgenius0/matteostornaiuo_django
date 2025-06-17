from django.db import models

from staff.models import Staff
from client.models import CompanyProfile

from users.models import User

from django.utils import timezone

# models for chat messages
class ChatRoom(models.Model):
    perticipants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat Room {self.id}'
    
    def get_room_group_name(self):
        return f'chat_room_{self.id}'
    
class ChatMessae(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f'Message from {self.sender.first_name} to {self.receiver.last_name} at {self.timestamp}'
    
    class Meta:
        ordering = ['-timestamp']


# class ChatList(models.Model):
#     me = models.ForeignKey(User, on_delete=models.CASCADE)
#     to = models.ForeignKey(User, on_delete=models.CASCADE)
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

