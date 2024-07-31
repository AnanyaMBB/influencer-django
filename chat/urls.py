from django.urls import path, include
from . import views



urlpatterns = [
    path("get", views.getChats, name="getChat"),
    path("create", views.createChat, name="createChat"),
    path("messages/get", views.getMessages, name="getMessages"),
    path("messages/create", views.createMessage, name="createMessage"),
]