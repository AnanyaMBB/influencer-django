from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

class ChatModel(models.Model):
    room_name = models.CharField(max_length=100)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    chat_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Message(models.Model):
    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now())