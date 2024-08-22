from . import models
from rest_framework import serializers
from django.contrib.auth.models import User

class TransacionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'