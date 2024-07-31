from channels.generic.websocket import AsyncWebsocketConsumer
import json 
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatModel, Message
import datetime

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"chat_{self.chat_id}"
        self.timestamp = datetime.datetime.now()
        if self.scope["query_string"]:
            self.query_parameters = dict(qs.split("=") for qs in self.scope["query_string"].decode("utf-8").split("&"))
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.query_parameters["user"] if self.query_parameters["user"] else "Anonymous"
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': str(self.timestamp)
        }))

        await self.save_message(message)

    @database_sync_to_async
    def save_message(self, message):
        chatModel = ChatModel.objects.get(id=self.chat_id)
        senderUser = User.objects.get(username=self.query_parameters["user"])
        message = Message(chat=chatModel, sender=senderUser, message=message, timestamp=self.timestamp)    
        message.save()