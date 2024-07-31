from django.shortcuts import render
from .models import ChatModel, Message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import ChatModelSerializer, MessageSerializer

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getChats(request): 
    user = User.objects.get(username=request.GET.get('username'))
    print(user, "USER")
    chatModel = ChatModel.objects.filter(
        Q(user1 = user) | Q(user2 = user)
    )
    
    serializer = ChatModelSerializer(chatModel, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def createChat(request):
    user1 = User.objects.get(username=request.data['user1'])
    user2 = User.objects.get(username=request.data['user2'])
    room_name = f"{request.data['user1']}-{request.data['user2']}"
    chatModel = ChatModel.objects.create(
        room_name=room_name,
        user1=user1,
        user2=user2
    )
    chatModel.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getMessages(request):
    # chat = ChatModel.objects.get(room_name=request.GET.get('room_name'))
    chat = ChatModel.objects.get(id=request.GET.get('chat_id'))
    messages = Message.objects.filter(chat=chat).order_by('-timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def createMessage(request):
    chat = ChatModel.objects.get(room_name=request.data['room_name'])
    sender = User.objects.get(username=request.data['sender'])
    message = Message.objects.create(
        chat=chat,
        sender=sender,
        message=request.data['message']
    )
    message.save()
    return Response(status=status.HTTP_201_CREATED)