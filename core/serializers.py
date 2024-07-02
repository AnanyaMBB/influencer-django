from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BusinessAccount, InfluencerAccount, InfluencerInstagramInformation, BaseService, UGCService, FeedPostService, StoryPostService, ReelPostService, OtherService

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

class BaseServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    class Meta:
        model = BaseService
        exclude=['instagram_information']

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=validated_data['instagram_id'])
        validated_data.pop('instagram_id')
        return BaseService.objects.create(instagram_information=instagramInformation, **validated_data)
        

class UGCServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    class Meta: 
        model = UGCService
        exclude=['instagram_information']

    def create(self, validated_data):
        print("validated_data", validated_data)
        instagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=validated_data['instagram_id'])
        validated_data.pop('instagram_id')
        return UGCService.objects.create(instagram_information=instagramInformation, **validated_data)

class UGCServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGCService
        fields = '__all__'

class FeedPostServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    class Meta: 
        model = FeedPostService
        exclude=['instagram_information']

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=validated_data['instagram_id'])
        validated_data.pop('instagram_id')
        return FeedPostService.objects.create(instagram_information=instagramInformation, **validated_data)
    
class FeedPostServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedPostService
        fields = '__all__'

class StoryPostServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    class Meta: 
        model = StoryPostService
        exclude=['instagram_information']

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=validated_data['instagram_id'])
        validated_data.pop('instagram_id')
        return StoryPostService.objects.create(instagram_information=instagramInformation, **validated_data)
    
class StoryPostServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryPostService
        fields = '__all__'

class ReelPostServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    class Meta: 
        model = ReelPostService
        exclude=['instagram_information']

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=validated_data['instagram_id'])
        validated_data.pop('instagram_id')
        return ReelPostService.objects.create(instagram_information=instagramInformation, **validated_data)
    
class ReelPostServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelPostService
        fields = '__all__'

class OtherServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    class Meta: 
        model = OtherService
        exclude=['instagram_information']
    
    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=validated_data['instagram_id'])
        validated_data.pop('instagram_id')
        return OtherService.objects.create(instagram_information=instagramInformation, **validated_data)
    
class OtherServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherService
        fields = '__all__'