from django.shortcuts import render
from .serializers import RegisterSerializer, InfluencerRegisterSerializer, InfluencerInstagramInformationSerializer, BaseServiceSerializer, UGCServiceSerializer, FeedPostServiceSerializer, StoryPostServiceSerializer, ReelPostServiceSerializer, OtherServiceSerializer, UGCServiceGetSerializer, FeedPostServiceGetSerializer, StoryPostServiceGetSerializer, ReelPostServiceGetSerializer, OtherServiceGetSerializer   
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import InfluencerAccount, InfluencerInstagramInformation, UGCService, FeedPostService, StoryPostService, ReelPostService, OtherService

@api_view(['POST'])
def businessRegister(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(tokens, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def influencerRegister(request):
    serializer = InfluencerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(tokens, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def influencerInstagramInformationAdd(request):
    serializer = InfluencerInstagramInformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def influencerInstagramInformationGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    influencerInstagramInformation = InfluencerInstagramInformation.objects.filter(influencer=influencerAccount)
    serializer = InfluencerInstagramInformationSerializer(influencerInstagramInformation, many=True)
    return Response({'accounts_info': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UGCServiceAdd(request):
    print(request.data)
    serializer = UGCServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UGCServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    ugcService = UGCService.objects.filter(instagram_information__influencer=influencerAccount)
    serializer = UGCServiceGetSerializer(ugcService, many=True)
    return Response({'ugc_services': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def FeedPostServiceAdd(request):
    serializer = FeedPostServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FeedPostServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    feedPostService = FeedPostService.objects.filter(instagram_information__influencer=influencerAccount)
    serializer = FeedPostServiceGetSerializer(feedPostService, many=True)
    return Response({'feed_services': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def StoryPostServiceAdd(request):
    serializer = StoryPostServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def StoryPostServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    storyPostService = StoryPostService.objects.filter(instagram_information__influencer=influencerAccount)
    serializer = StoryPostServiceGetSerializer(storyPostService, many=True)
    return Response({'story_services': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ReelPostServiceAdd(request):
    serializer = ReelPostServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ReelPostServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    reelPostService = ReelPostService.objects.filter(instagram_information__influencer=influencerAccount)
    serializer = ReelPostServiceGetSerializer(reelPostService, many=True)
    return Response({'reel_services': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def OtherServiceAdd(request):
    serializer = OtherServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def OtherServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    otherService = OtherService.objects.filter(instagram_information__influencer=influencerAccount)
    serializer = OtherServiceGetSerializer(otherService, many=True)
    return Response({'other_services': serializer.data})



    

