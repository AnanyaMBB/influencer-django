from django.urls import path 
from .consumers import ChatRoomConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:chat_id>/', ChatRoomConsumer.as_asgi()),
]