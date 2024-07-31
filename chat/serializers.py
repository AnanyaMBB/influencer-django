from rest_framework import serializers
from .models import ChatModel, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'  

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['sender'] = instance.sender.username
        return ret

class ChatModelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ChatModel
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user1'] = instance.user1.username
        ret['user2'] = instance.user2.username

        last_message = Message.objects.filter(chat=instance).order_by('timestamp').last()
        ret["last_message"] = last_message.message
        ret["last_message_timestamp"] = last_message.timestamp
        return ret

