from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BusinessAccount, InfluencerAccount, InfluencerInstagramInformation

class businessAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAccount
        # fields = '__all__'
        exclude=['user']

class RegisterSerializer(serializers.ModelSerializer):
    businessAccount = businessAccountSerializer()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'businessAccount']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        business_data = validated_data.pop('businessAccount')
        user = User.objects.create_user(**validated_data)
        BusinessAccount.objects.create(user=user, **business_data)
        return user
    
class InfluencerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerAccount
        exclude=['user']

class InfluencerRegisterSerializer(serializers.ModelSerializer):
    influencerAccount = InfluencerAccountSerializer()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'influencerAccount']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        influencer_data = validated_data.pop('influencerAccount')
        user = User.objects.create_user(**validated_data)
        InfluencerAccount.objects.create(user=user, **influencer_data)
        return user
    
class InfluencerInstagramInformationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)
    class Meta:
        model = InfluencerInstagramInformation
        exclude=['influencer']
        
    
    def create(self, validated_data):        
        user = User.objects.get(username=validated_data['user'])
        validated_data.pop('user')
        influencer = InfluencerAccount.objects.get(user=user)
        return InfluencerInstagramInformation.objects.create(influencer=influencer, **validated_data)

class InfluencerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerInstagramInformation
        fields = '__all__'