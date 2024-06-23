from django.shortcuts import render
from .serializers import RegisterSerializer, InfluencerRegisterSerializer, InfluencerInstagramInformationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import InfluencerAccount, InfluencerInstagramInformation

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


    

