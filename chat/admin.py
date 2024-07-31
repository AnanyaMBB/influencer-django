from django.contrib import admin
from .models import ChatModel, Message

# Register your models here.
admin.site.register(ChatModel)
admin.site.register(Message)
