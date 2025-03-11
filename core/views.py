from django.shortcuts import render, get_object_or_404, Http404
from . import serializers
from .serializers import (
    RegisterSerializer,
    InfluencerAccountSerializer,
    InfluencerRegisterSerializer,
    InfluencerInstagramInformationSerializer,
    BaseServiceSerializer,
    UGCServiceSerializer,
    FeedPostServiceSerializer,
    StoryPostServiceSerializer,
    ReelPostServiceSerializer,
    OtherServiceSerializer,
    UGCServiceGetSerializer,
    FeedPostServiceGetSerializer,
    StoryPostServiceGetSerializer,
    ReelPostServiceGetSerializer,
    OtherServiceGetSerializer,
    InstagramDetailsSerializer,
    InstagramMediaDataSerializer,
    InstagramAgeDemographicsSerializer,
    InstagramGenderDemographicsSerializer,
    InstagramCityDemographicsSerializer,
    InstagramCountryDemographicsSerializer,
    InstagramInformationSerializer,
    ContractCreateSerializer,
    ContractSerializer,
    ContractVersionCreateSerializer,
    ContractVersionSerializer,
    ContractVersionTextUpdateSerializer,
    SignatureRequestsSerializer,
    SignatureRequestsCreateSerializer,
    UserFilesSerializer,
    ServiceSerializer,
    RequestsSerializer
    # TikTokAccountSerializer,
    # TikTokAccountInformationSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import (
    InfluencerAccount,
    BusinessAccount,
    InfluencerInstagramInformation,
    UGCService,
    FeedPostService,
    StoryPostService,
    ReelPostService,
    OtherService,
    InstagramDetails,
    InstagramMediaData,
    InstagramAgeDemographics,
    InstagramGenderDemographics,
    InstagramCityDemographics,
    InstagramCountryDemographics,
    InstagramInitialInformation,
    InstagramDetails,
    Contract,
    ContractVersion,
    ContractUserPermissions,
    ContractVersionUserPermissions,
    SignatureRequests,
    Files,
    Service,
    ServicePricing,
    Requests
    # TikTokAccount, 
    # TikTokAccountInformation
)
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .filters import InfluencerFilter
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django.db.models import Max, Min
from rest_framework import generics
from django.http import JsonResponse, FileResponse
from django.core.serializers import serialize
from django.db.models import OuterRef, Subquery, F
from django.db.models import Q, Exists, OuterRef
from django.db.models.functions import Coalesce
from django.forms.models import model_to_dict
from django_countries.fields import Country
from datetime import datetime
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.core.files.storage import default_storage
import requests
import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import MetadataQuery
from weaviate.classes.query import Filter

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta

from .models import (
    YouTubeChannelInformation,
    YouTubeChannelAnalytics,
    YouTubeVideoInformation,
    YouTubeVideoAnalytics,
    YouTubeGenderDemographics,
    YouTubeAgeDemographics,
    YouTubeGeographicDemographics
)

import base64

from . import filters
from chat.models import ChatModel


@api_view(["POST"])
def businessRegister(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return Response(tokens, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def influencerRegister(request):
    serializer = InfluencerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        print(f"New User Created: {user.id}")
        refresh = RefreshToken.for_user(user)
        tokens = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return Response(tokens, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def accountType(request):
    username = request.GET.get("username")
    user = User.objects.get(username=username)

    print(InfluencerAccount.objects.filter(user=user))
    print(BusinessAccount.objects.filter(user=user))
    print(InfluencerAccount.objects.filter(user=user).exists())
    print(BusinessAccount.objects.filter(user=user).exists())
    if InfluencerAccount.objects.filter(user=user).exists():
        return Response({"accountType": "influencer"})
    elif BusinessAccount.objects.filter(user=user).exists():
        return Response({"accountType": "business"})
    return Response({"account_type": "none"})


@api_view(["POST"])
def influencerInstagramInformationAdd(request):
    serializer = InfluencerInstagramInformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def influencerInstagramInformationGet(request):
    user = User.objects.get(username=request.GET.get("username"))
    influencerAccount = InfluencerAccount.objects.get(user=user)
    influencerInstagramInformation = InfluencerInstagramInformation.objects.filter(
        influencer=influencerAccount
    )
    serializer = InfluencerInstagramInformationSerializer(
        influencerInstagramInformation, many=True
    )
    return Response({"accounts_info": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def UGCServiceAdd(request):
    print(request.data)
    serializer = UGCServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def UGCServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    ugcService = UGCService.objects.filter(
        instagram_information__influencer=influencerAccount
    )
    serializer = UGCServiceGetSerializer(ugcService, many=True)
    return Response({"ugc_services": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def FeedPostServiceAdd(request):
    serializer = FeedPostServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def FeedPostServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    feedPostService = FeedPostService.objects.filter(
        instagram_information__influencer=influencerAccount
    )
    serializer = FeedPostServiceGetSerializer(feedPostService, many=True)
    return Response({"feed_services": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def StoryPostServiceAdd(request):
    serializer = StoryPostServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def StoryPostServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    storyPostService = StoryPostService.objects.filter(
        instagram_information__influencer=influencerAccount
    )
    serializer = StoryPostServiceGetSerializer(storyPostService, many=True)
    return Response({"story_services": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ReelPostServiceAdd(request):
    serializer = ReelPostServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ReelPostServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    reelPostService = ReelPostService.objects.filter(
        instagram_information__influencer=influencerAccount
    )
    serializer = ReelPostServiceGetSerializer(reelPostService, many=True)
    return Response({"reel_services": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def OtherServiceAdd(request):
    serializer = OtherServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def OtherServiceGet(request):
    user = User.objects.get(username=request.user)
    influencerAccount = InfluencerAccount.objects.get(user=user)
    otherService = OtherService.objects.filter(
        instagram_information__influencer=influencerAccount
    )
    serializer = OtherServiceGetSerializer(otherService, many=True)
    return Response({"other_services": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def InstagramDetailsGet(request):
    print(request.GET)
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=request.GET["instagram_id"]
    )
    instagramDetails = InstagramDetails.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    )
    serializer = InstagramDetailsSerializer(instagramDetails, many=True)
    return Response({"instagram_details": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def InstagramMediaDataGet(request):
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=request.GET["instagram_id"]
    )
    instagramMediaData = InstagramMediaData.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    )
    serializer = InstagramMediaDataSerializer(instagramMediaData, many=True)
    return Response({"instagram_media_data": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def InstagramAgeDemographicsGet(request):
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=request.GET["instagram_id"]
    )
    instagramAgeDemographics = InstagramAgeDemographics.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    )
    serializer = InstagramAgeDemographicsSerializer(instagramAgeDemographics, many=True)
    return Response({"instagram_age_demographics": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def InstagramGenderDemographicsGet(request):
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=request.GET["instagram_id"]
    )
    instagramGenderDemographics = InstagramGenderDemographics.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    )
    serializer = InstagramGenderDemographicsSerializer(
        instagramGenderDemographics, many=True
    )
    return Response({"instagram_gender_demographics": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def InstagramCityDemographicsGet(request):
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=request.GET["instagram_id"]
    )
    instagramCityDemographics = InstagramCityDemographics.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    )
    serializer = InstagramCityDemographicsSerializer(
        instagramCityDemographics, many=True
    )
    return Response({"instagram_city_demographics": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def InstagramCountryDemographicsGet(request):
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=request.GET["instagram_id"]
    )
    instagramCountryDemographics = InstagramCountryDemographics.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    )
    serializer = InstagramCountryDemographicsSerializer(
        instagramCountryDemographics, many=True
    )
    return Response({"instagram_country_demographics": serializer.data})


def valid_query_param(param):
    return param != "" and param is not None


def convert_datetime(dt):
    return dt.isoformat() if isinstance(dt, datetime) else dt


def convert_country(country):
    print(f"country entered: {country}")
    return str(country) if isinstance(country, Country) else country


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def InstagramFilterView(request):
    print("HERE")
    queryset = filter_influencers(location="Philadelphia", followers=100)

    #  {"influencer": 2, "instagram_id": "17841439310660818", "long_access_token": "EAANjVrzUSWkBO68AmxkC65NU7lVXzhlaoQHrNZApRjuTiaCQZBZBIDuoCS0cUPljLAUSYMSV3UUAHlyQ2IvBOg0eqcQb4K7tpTzH17IHvo6wQw6keoxuXgGKSiIfbFKlmsGp7fccF4m4OFkCAljQZBhrA65rabw7JUA0a1w3AmY5FLDN7L4rXcdAd3vfqCPN"}}]
    response = []
    responseDict = {}
    for influencer in queryset:
        responseDict["influencer"] = influencer.influencer.id
        responseDict["instagram_id"] = influencer.instagram_id

        instagramInitialInformation = (
            InstagramInitialInformation.objects.filter(
                influencer_instagram_information=influencer
            )
            .order_by("-date")
            .first()
        )
        if instagramInitialInformation:
            responseDict["instagram_initial_information"] = model_to_dict(
                instagramInitialInformation
            )

        instagramCountryDemographics = (
            InstagramCountryDemographics.objects.filter(
                influencer_instagram_information=influencer
            )
            .order_by("-this_week_follower_count")
            .first()
        )
        if instagramCountryDemographics:
            country_demographics = model_to_dict(instagramCountryDemographics)
            # Convert Country and datetime objects
            for key, value in country_demographics.items():
                country_demographics[key] = convert_country(convert_datetime(value))
            responseDict["instagram_country_demographics"] = country_demographics

        response.append(responseDict)
        responseDict = {}

    return JsonResponse(response, safe=False)


def filter_influencers(
    name=None, username=None, followers=None, price=None, location=None
):
    queryset = InfluencerInstagramInformation.objects.all()

    # Filter by name from User model
    if name:
        queryset = queryset.filter(influencer__user__name__icontains=name)

    # Filter by username from InstagramInitialInformation
    if username:
        username_subquery = (
            InstagramInitialInformation.objects.filter(
                influencer_instagram_information=OuterRef("pk"),
                username__icontains=username,
            )
            .order_by("-date")
            .values("pk")[:1]
        )

        queryset = queryset.filter(Exists(username_subquery))
        queryset = queryset.annotate(
            latest_username_date=Subquery(username_subquery.values("date"))
        ).order_by("-latest_username_date")

    # Filter by followers from InstagramInitialInformation
    if followers:
        latest_followers_subquery = (
            InstagramInitialInformation.objects.filter(
                influencer_instagram_information=OuterRef("pk")
            )
            .order_by("-date")
            .values("followers_count")[:1]
        )

        queryset = queryset.annotate(
            latest_followers=Subquery(latest_followers_subquery)
        ).filter(latest_followers__gte=followers)

    # Filter by price from Services model
    if price:
        queryset = queryset.filter(
            Exists(
                Services.objects.filter(
                    influencer__influencerinstagraminformation=OuterRef("pk"),
                    price__lte=price,
                )
            )
        )

    # Filter by Audience Location (City or Country)
    if location:
        city_subquery = (
            InstagramCityDemographics.objects.filter(
                influencer_instagram_information=OuterRef("pk"),
                this_week_city__icontains=location,
            )
            .order_by("-this_week_follower_count")
            .values("pk")[:1]
        )

        country_subquery = (
            InstagramCountryDemographics.objects.filter(
                influencer_instagram_information=OuterRef("pk"),
                this_week_country__icontains=location,
            )
            .order_by("-this_week_follower_count")
            .values("pk")[:1]
        )

        queryset = queryset.filter(
            Q(Exists(city_subquery)) | Q(Exists(country_subquery))
        )
        queryset = queryset.annotate(
            location_followers=Coalesce(
                Subquery(city_subquery.values("this_week_follower_count")),
                Subquery(country_subquery.values("this_week_follower_count")),
                0,
            )
        ).order_by("-location_followers")

    return queryset


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createContract(request):
    serializer = ContractCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getContractAll(request):
    try:
        contract = Contract.objects.all()
        serializer = ContractSerializer(contract, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Contract.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getContract(request):
    try:
        contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
        serializer = ContractSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Contract.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getContractByAccount(request):
    try: 
        contract = models.Contract.objects.get(business__user__username=request.GET.get("username"),
                                        phyllo_added_account__phyllo_accountid=request.GET.get("account_id"))
        serializer = serializers.ContractSerializer(contract)                                    
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Contract.DoesNotExist:
        return Response({"error": "Contract Doesnot Exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def createNewVersion(request):
    print("request data: ", request.data)
    serializer = ContractVersionCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getContractVersions(request):
    contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    contractVersions = ContractVersion.objects.filter(contract=contract)
    serializer = ContractVersionSerializer(contractVersions, many=True)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def getContractVersionsByAccount(request): 
    contractVersions = ContractVersion.objects.filter(contract__business__user__username=request.GET.get("username"), contract__phyllo_added_account__phyllo_accountid=request.GET.get("account_id"))
    serializer = serializers.ContractVersionByAccountSerializer(contractVersions, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getContractVersionText(request):
    contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    contractVersion = ContractVersion.objects.get(
        contract=contract, contract_version=request.GET.get("version_id")
    )
    print(f"Contract Version: {contractVersion}")
    serializer = ContractVersionSerializer(contractVersion)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updateContractVersionText(request):
    contract = Contract.objects.get(contract_id=request.data.get("contract_id"))
    contractVersion = ContractVersion.objects.get(
        contract=contract, contract_version=request.data.get("version_id")
    )
    serializer = ContractVersionTextUpdateSerializer(contractVersion, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def addSignatureRequest(request):
    serializer = SignatureRequestsCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getSignatureState(request):
    contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    contractVersion = ContractVersion.objects.get(
        contract=contract, contract_version=request.GET.get("version_id")
    )

    signatureRequests = (
        SignatureRequests.objects.filter(
            contract=contract, contract_version=contractVersion
        )
        .order_by("-request_date")
        .first()
    )
    serializer = SignatureRequestsSerializer(signatureRequests)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def acceptSignature(request):
    # try:

    contract = Contract.objects.get(contract_id=request.data.get("contract_id"))
    contractVersion = ContractVersion.objects.get(
        contract=contract, contract_version=request.data.get("version_id")
    )
    user = User.objects.get(username=request.data.get("username"))

    signatureRequests = SignatureRequests.objects.get(
        contract=contract,
        contract_version=contractVersion,
        request_user=user,
        request_date=request.data.get("request_date"),
    )
    signatureRequests.state = "accepted"
    signatureRequests.save()
    return Response(status=status.HTTP_200_OK)
    # except SignatureRequests.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    # except Exception as e:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def declineSignature(request):
    try:
        contract = Contract.objects.get(contract_id=request.data.get("contract_id"))
        contractVersion = ContractVersion.objects.get(
            contract=contract, contract_version=request.data.get("version_id")
        )
        user = User.objects.get(username=request.data.get("username"))

        signatureRequests = SignatureRequests.objects.get(
            contract=contract,
            contract_version=contractVersion,
            request_user=user,
            request_date=request.data.get("request_date"),
        )
        signatureRequests.state = "declined"
        signatureRequests.save()
        return Response(status=status.HTTP_200_OK)
    except SignatureRequests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def uploadDocumentSignNow(request):
    try:
        signnow_access_token = ""
        # Get Oauth token
        url = "https://api.signnow.com/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {settings.SIGNNOW_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "username": f"{settings.SIGNNOW_EMAIL}",
            "password": f"{settings.SIGNNOW_PASSWORD}",
            "grant_type": "password",
            "scope": "*",
        }

        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        response.raise_for_status()
        signnow_access_token = response.json()["access_token"]

        # Upload Document
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        url = "https://api.signnow.com/document"
        headers = {
            "Authorization": f"Bearer {signnow_access_token}",
        }
        files = {
            "file": (file.name, file.read(), file.content_type),
        }

        response = requests.post(url, headers=headers, files=files)
        contract = Contract.objects.get(contract_id=request.data.get("contract_id"))
        contract.document_id = response.json()["id"]
        contract.save()

        phylloScheduledPosts = models.PhylloScheduledPost.objects.filter(campaign_influencers=contract.campaign_influencer)
        for scheduled in phylloScheduledPosts: 
            scheduled.document_id = response.json()["id"]
            scheduled.save()
        # phylloScheduledPost.document_id = response.json()["id"]
        # phylloScheduledPost.save()
        print(response.json())
        response.raise_for_status()
        return Response(response.json(), status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def inviteSignNow(request):
    signnow_access_token = ""
    # Get Oauth token
    url = "https://api.signnow.com/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {settings.SIGNNOW_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "username": f"{settings.SIGNNOW_EMAIL}",
        "password": f"{settings.SIGNNOW_PASSWORD}",
        "grant_type": "password",
        "scope": "*",
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    response.raise_for_status()
    signnow_access_token = response.json()["access_token"]

    contract = Contract.objects.get(contract_id=request.data.get("contract_id"))
    document_id = contract.document_id
    business_email = contract.business.user.email
    influencer_email = contract.phyllo_added_account.phyllo_account.phyllo_account.user.email

    webhook_response = register_signnow_webhook(signnow_access_token, document_id)
    

    # Invite to sign document
    subject = "Sign this document"
    message = "Sign this document"

    url = f"https://api.signnow.com/document/{document_id}/invite"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {signnow_access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "document_id": document_id,
        "to": business_email,
        "from": settings.SIGNNOW_EMAIL,
        "subject": subject,
        "message": message,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    webhook_response_2 = register_signnow_webhook(signnow_access_token, document_id)

    url = f"https://api.signnow.com/document/{document_id}/invite"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {signnow_access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "document_id": document_id,
        "to": influencer_email,
        "from": settings.SIGNNOW_EMAIL,
        "subject": subject,
        "message": message,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return Response(response.json(), status=status.HTTP_200_OK)


def register_signnow_webhook(signnow_access_token, document_id):
    url = "https://api.signnow.com/event_subscription"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {signnow_access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "event": "document.complete",
        "entity_id": document_id,  # Attach to specific document
        "callback_url": "https://fdcd-79-110-55-8.ngrok-free.app/api/signnow/webhook/",
        "secret_key": settings.SIGNNOW_WEBHOOK_SECRET
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()  # Returns the webhook details


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def inviteSignNow(request):
#     signnow_access_token = ""

#     # Get OAuth token
#     url = "https://api.signnow.com/oauth2/token"
#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Basic {settings.SIGNNOW_API_KEY}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "username": settings.SIGNNOW_EMAIL,
#         "password": settings.SIGNNOW_PASSWORD,
#         "grant_type": "password",
#         "scope": "*",
#     }

#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
#     signnow_access_token = response.json()["access_token"]

#     # Fetch contract details
#     contract = Contract.objects.get(contract_id=request.data.get("contract_id"))
#     document_id = contract.document_id
#     business_email = contract.business.user.email
#     influencer_email = contract.phyllo_added_account.phyllo_account.phyllo_account.user.email

#     # **Step 1: Register Webhook**
#     webhook_response = register_signnow_webhook(signnow_access_token, document_id)

#     # Define subject and message
#     subject = "Sign this document"
#     message = "Sign this document"

#     # **Step 2: Invite signers**
#     url = f"https://api.signnow.com/document/{document_id}/invite"
#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {signnow_access_token}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "document_id": document_id,
#         "from": settings.SIGNNOW_EMAIL,
#         "subject": subject,
#         "message": message,
#         "to": [
#             {
#                 "email": business_email,
#                 "role_id": "ROLE_ID_HERE",
#                 "order": 1,
#                 "redirect_uri": "https://yourapp.com/signed-successfully"
#             },
#             {
#                 "email": influencer_email,
#                 "role_id": "ROLE_ID_HERE",
#                 "order": 2,
#                 "redirect_uri": "https://yourapp.com/signed-successfully"
#             }
#         ]
#     }

#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()

#     return Response({
#         "invite_response": response.json(),
#         "webhook_response": webhook_response
#     }, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getSignedContracts(request):
    signedRequests = SignatureRequests.objects.filter(state="accepted")
    serializer = SignatureRequestsSerializer(signedRequests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getSignedContract(request):
    contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    print("Contract: ", contract)
    contractVersion = ContractVersion.objects.get(
        contract=contract, contract_version=request.GET.get("version_id")
    )
    print("Contract Version: ", contractVersion)
    signedRequests = SignatureRequests.objects.get(
        contract=contract, contract_version=contractVersion, state="accepted"
    )
    serializer = SignatureRequestsSerializer(signedRequests)
    return Response(serializer.data, status=status.HTTP_200_OK)

import json
import hmac
import hashlib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
# from .models import Document  # Adjust this import to match your database model

@api_view(["POST"])
def signnow_webhook(request):
    try:
        # Verify the signature (if SignNow provides one)
        secret = settings.SIGNNOW_WEBHOOK_SECRET.encode()
        signature = request.headers.get("X-SignNow-Signature", "")
        body = request.body
        print("body: ", body)
        expected_signature = hmac.new(secret, body, hashlib.sha256).hexdigest()
        
        if signature and not hmac.compare_digest(expected_signature, signature):
            return Response({"error": "Invalid signature"}, status=403)

        data = json.loads(body)
        print("JSON data: ", data)
        event_type = data.get("meta").get("event")
        document_id = data.get("content", {}).get("document_id")
        print("event type: ", event_type)
        print("document_id: ", document_id) 


        if event_type == "document.complete" and document_id:
            document_details = getDocumentDetails(document_id)
            print("document_details: ", document_details)
            phylloScheduledPosts = models.PhylloScheduledPost.objects.filter(document_id=document_id)
            for scheduled in phylloScheduledPosts:                 
                if document_details: 
                    signatures = document_details.get("signatures", None)
                    print("Signatures: ", signatures)
                    if signatures: 
                        for signature in signatures: 
                            signature_email = signature.get("email", None) 
                            if signature_email: 
                                if models.BusinessAccount.objects.filter(user__email=signature_email).exists(): 
                                    scheduled.business_contract_signed = True
                                elif models.InfluencerAccount.objects.filter(user__email=signature_email).exists():
                                    scheduled.influencer_contract_signed = True
                                scheduled.save()
                                return Response({"status": "success"}, status=200)            

        return Response({"status": "ignored"}, status=400)
    except Exception as e:
        print("Error: ", e)
        return Response({"error": str(e)}, status=500)

def getDocumentDetails(document_id):
    try: 
        signnow_access_token = ""
        # Get Oauth token
        url = "https://api.signnow.com/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {settings.SIGNNOW_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "username": f"{settings.SIGNNOW_EMAIL}",
            "password": f"{settings.SIGNNOW_PASSWORD}",
            "grant_type": "password",
            "scope": "*",
        }

        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        response.raise_for_status()
        signnow_access_token = response.json()["access_token"]

        

        url = f"https://api.signnow.com/document/{document_id}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {signnow_access_token}",
            "Content-Type": "application/json",
        }
        
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e: 
        pass



@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def uploadFile(request):
    user = User.objects.get(username=request.data.get("username"))
    file = request.FILES.get("file")
    print("File: >", file.name)
    file_instance = Files(file=file, file_name=file.name, file_size=file.size)
    file_instance.save()
    file_instance.users.add(user)

    response = {"file_id": file_instance.id}

    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getUserFiles(request):
    try:
        user = User.objects.get(username=request.GET.get("username"))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    # contract_version = ContractVersion.objects.get(
    #     contract=contract, contract_version=request.GET.get("version_id")
    # )

    # serializer = UserFilesSerializer(
    #     user, context={"contract": contract, "contract_version": contract_version}
    # )

    serializer = UserFilesSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getContractFile(request):
    contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    contract_version = ContractVersion.objects.get(
        contract=contract, contract_version=request.GET.get("version_id")
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def downloadFile(request):
    file_instance = get_object_or_404(Files, id=request.GET.get("file_id"))
    file_path = file_instance.file.path

    try:
        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename=file_instance.file_name or file_instance.file.name,
        )
    except FileNotFoundError:
        raise Http404("File does not exist")


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getElementDetails(request):
    # try:
    contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    contract_version = ContractVersion.objects.get(
        contract=contract, contract_version=request.GET.get("version_id")
    )
    
    # influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
    #     instagram_id=contract.influencerInstagramInformation.instagram_id
    # )
    # instagramInitialInformation = InstagramInitialInformation.objects.filter(
    #     influencer_instagram_information=influencerInstagramInformation
    # ).latest("date")
    return_data = {
        "company_name": contract.business.company_name,
        "influencer_name": contract.phyllo_added_account.phyllo_account.phyllo_account.user.get_full_name(),
        "influencer_username": models.PhylloAccountProfile.objects.filter(phyllo_account=contract.phyllo_added_account)[0].phyllo_account_platform_username,
        "file_upload_date": contract_version.file_upload_date,
        "file_upload_user": contract_version.file_uploader,
    }

    return Response(return_data, status=status.HTTP_200_OK)
    # except Exception as e:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def updateCampaignFile(request):
    contract = Contract.objects.get(contract_id=request.data.get("contract_id"))
    contract_version = ContractVersion.objects.get(
        contract=contract, contract_version=request.data.get("version_id")
    )
    signatureRequests = SignatureRequests.objects.filter(
        contract=contract, contract_version=contract_version
    ).latest("request_date")

    file = Files.objects.get(id=request.data.get("file_id"))
    signatureRequests.file = file
    signatureRequests.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def addInstagramService(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getInstagramService(request):
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=request.GET.get("instagram_id")
    )
    services = Service.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    )
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getRequests(request):
    requests = Requests.objects.filter(
        influencer__user__username=request.GET.get("username")
    ).order_by("-request_date")
    serializer = RequestsSerializer(requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def sendRequests(request):
    serializer = RequestsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def updateRequestState(request):
    requests = Requests.objects.get(id=request.data.get("request_id"))
    requests.state = request.data.get("state")
    requests.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def searchReels(request):
    print("QUERY: ", request.GET.get("query"))
    print("TOKENS: ", request.GET.get("tokens"))
    headers = {"X-OpenAI-Api-Key": settings.OPENAI_API_KEY}
    weaviateClient = weaviate.connect_to_wcs(
        cluster_url=settings.WEAVIATE_CLUSTER_URL,
        auth_credentials=weaviate.auth.AuthApiKey(api_key=settings.WEAVIATE_API_KEY),
        headers=headers,
    )

    # try:
    if weaviateClient.is_ready():
        if request.GET.get("platform") == "instagram": 
            transcriptions = weaviateClient.collections.get("ReelsTranscript")

            tokensList = request.GET.get("tokens").split(",")
            filtersList = []
            print("TOKENS LIST: ", tokensList)  
            usernamesList = request.GET.get("username").split(",")
            print("USERNAMES LIST: ", usernamesList)
            if request.GET.get("username") != "" and request.GET.get("username") != None and len(usernamesList) > 0 and usernamesList[0] != "": 
                filtersList.append(
                    Filter.by_property("username").contains_any(usernamesList)
                )   
            if request.GET.get("audio_id") != "" and request.GET.get("audio_id") != None:
                filtersList.append(
                    Filter.by_property("audio_id").equal(request.GET.get("audio_id"))
                )
            if (
                request.GET.get("likes_count") != ""
                and request.GET.get("likes_count") != None
            ):
                filtersList.append(
                    Filter.by_property("likes_count").greater_than(
                        int(request.GET.get("likes_count"))
                    )
                )
            if (
                request.GET.get("comments_count") != ""
                and request.GET.get("comments_count") != None
            ):
                filtersList.append(
                    Filter.by_property("comments_count").greater_than(
                        int(request.GET.get("comments_count"))
                    )
                )


            if request.GET.get("query") == "" or request.GET.get("query") == None:
                if len(tokensList) > 0 and tokensList[0] != "":
                    response = transcriptions.query.fetch_objects(
                        filters=(
                            Filter.all_of(filtersList)
                            & ((Filter.by_property("transcript").contains_all(tokensList))
                            | (Filter.by_property("caption").contains_all(tokensList)))
                        ),
                        return_metadata=wvc.query.MetadataQuery(certainty=True),
                    )
                else:
                    print("FILTERS LIST: ", filtersList)
                    response = transcriptions.query.fetch_objects(
                        filters=(Filter.all_of(filtersList)),
                        return_metadata=wvc.query.MetadataQuery(certainty=True),
                    )

            else:
                if len(tokensList) > 0 and tokensList[0] != "":
                    if len(filtersList) > 0:
                        response = transcriptions.query.near_text(
                            query=request.GET.get("query"),
                            filters=(
                                Filter.all_of(filtersList)
                                & ((
                                    Filter.by_property("transcript").contains_all(
                                        tokensList
                                    )
                                )
                                | (Filter.by_property("caption").contains_all(tokensList)))
                            ),
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )
                    else:
                        print("TOKENS LIST ERROR: ", tokensList)
                        print("QUERY ERROR: ", request.GET.get("query"))
                        
                        response = transcriptions.query.near_text(
                            query=request.GET.get("query"),
                            filters=(
                                (
                                    Filter.by_property("transcript").contains_all(
                                        tokensList
                                    )
                                )
                                | (Filter.by_property("caption").contains_all(tokensList))
                            ),
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )
                else:
                    if len(filtersList) > 0:
                        response = transcriptions.query.near_text(
                            query=request.GET.get("query"),
                            filters=(Filter.all_of(filtersList)),
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )
                    else:
                        response = transcriptions.query.near_text(
                            query=request.GET.get("query"),
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )
            searchResult = [object.properties for object in response.objects]
            weaviateClient.close()
            return Response(searchResult, status=status.HTTP_200_OK)
        elif request.GET.get("platform") == "youtube":
            transcriptions = weaviateClient.collections.get("ChannelShortsTranscript")

            tokensList = request.GET.get("tokens").split(",")
            filtersList = []
            usernamesList = request.GET.get("username").split(",")
            if request.GET.get("username") != "" and request.GET.get("username") != None and len(usernamesList) > 0 and usernamesList[0] != "": 
                filtersList.append(
                    Filter.by_property("username").contains_any(usernamesList)
                )   
            if request.GET.get("audio_id") != "" and request.GET.get("audio_id") != None:
                filtersList.append(
                    Filter.by_property("audio_id").equal(request.GET.get("audio_id"))
                )
            if (
                request.GET.get("likes_count") != ""
                and request.GET.get("likes_count") != None
            ):
                filtersList.append(
                    Filter.by_property("likes_count").greater_than(
                        int(request.GET.get("likes_count"))
                    )
                )
            if (
                request.GET.get("comments_count") != ""
                and request.GET.get("comments_count") != None
            ):
                filtersList.append(
                    # Filter.by_property("comments_count").greater_than("{:,}".format(int(request.GET.get("comments_count"))))
                    Filter.by_property("comments_count").greater_than(int(request.GET.get("comments_count")))
                )
            
            if request.GET.get("language") != "" and request.GET.get("language") != None:
                if request.GET.get("language") == "en":
                    filtersList.append(
                        Filter.by_property("language").equal(request.GET.get("language"))
                    )
                else: 
                    filtersList.append(
                        Filter.by_property("language").not_equal("en")
                    )

            if request.GET.get("action") == "" or request.GET.get("action") == None:
                if request.GET.get("query") == "" or request.GET.get("query") == None:                
                    if len(tokensList) > 0 and tokensList[0] != "":
                        response = transcriptions.query.fetch_objects(
                            filters=(
                                Filter.all_of(filtersList)
                                & ((Filter.by_property("transcript").contains_all(tokensList))
                                | (Filter.by_property("caption").contains_all(tokensList)))
                            ),
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )
                    else:
                        response = transcriptions.query.fetch_objects(
                            filters=(Filter.all_of(filtersList)),
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )

                else:
                    if len(tokensList) > 0 and tokensList[0] != "":
                        if len(filtersList) > 0:
                            response = transcriptions.query.near_text(
                                query=request.GET.get("query"),
                                filters=(
                                    Filter.all_of(filtersList)
                                    & ((
                                        Filter.by_property("transcript").contains_all(
                                            tokensList
                                        )
                                    )
                                    | (Filter.by_property("caption").contains_all(tokensList)))
                                ),
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                        else:
                            response = transcriptions.query.near_text(
                                query=request.GET.get("query"),
                                filters=(
                                    (
                                        Filter.by_property("transcript").contains_all(
                                            tokensList
                                        )
                                    )
                                    | (Filter.by_property("caption").contains_all(tokensList))
                                ),
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                    else:
                        
                        if len(filtersList) > 0:
                            response = transcriptions.query.near_text(
                                query=request.GET.get("query"),
                                filters=(Filter.all_of(filtersList)),
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                        else:
                            response = transcriptions.query.near_text(
                                query=request.GET.get("query"),
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                searchResult = [object.properties for object in response.objects]
                weaviateClient.close()
                return Response(searchResult, status=status.HTTP_200_OK)
            else:
                action = request.GET.get("action") + ". Return the response in html form : {transcript}" 
                if request.GET.get("query") == "" or request.GET.get("query") == None:                
                    if len(tokensList) > 0 and tokensList[0] != "":
                        response = transcriptions.query.fetch_objects(
                            filters=(
                                Filter.all_of(filtersList)
                                & ((Filter.by_property("transcript").contains_all(tokensList))
                                | (Filter.by_property("caption").contains_all(tokensList)))
                            ),
                            single_prompt=action,
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )
                    else:
                        response = transcriptions.query.fetch_objects(
                            filters=(Filter.all_of(filtersList)),
                            single_prompt=action,
                            return_metadata=wvc.query.MetadataQuery(certainty=True),
                        )

                else:
                    if len(tokensList) > 0 and tokensList[0] != "":
                        if len(filtersList) > 0:
                            response = transcriptions.generate.near_text(
                                query=request.GET.get("query"),
                                filters=(
                                    Filter.all_of(filtersList)
                                    & ((
                                        Filter.by_property("transcript").contains_all(
                                            tokensList
                                        )
                                    )
                                    | (Filter.by_property("caption").contains_all(tokensList)))
                                ),
                                single_prompt=action,
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                        else:
                            response = transcriptions.generate.near_text(
                                query=request.GET.get("query"),
                                filters=(
                                    (
                                        Filter.by_property("transcript").contains_all(
                                            tokensList
                                        )
                                    )
                                    | (Filter.by_property("caption").contains_all(tokensList))
                                ),
                                single_prompt=action,
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                    else:
                        
                        if len(filtersList) > 0:
                            response = transcriptions.generate.near_text(
                                query=request.GET.get("query"),
                                filters=(Filter.all_of(filtersList)),
                                single_prompt=action,
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                        else:
                            response = transcriptions.generate.near_text(
                                query=request.GET.get("query"),
                                single_prompt=action,
                                return_metadata=wvc.query.MetadataQuery(certainty=True),
                            )
                searchResult = [{**object.properties, "generated":object.generated} for object in response.objects]
                weaviateClient.close()
                return Response(searchResult, status=status.HTTP_200_OK)



    # except Exception as e:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    # finally:
    #     weaviateClient.close()


from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

def exchange_auth_code_for_tokens(auth_code):
    try: 
        flow = Flow.from_client_secrets_file(
            './client_secret.json',  # Update with the path to your client secret file
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/yt-analytics.readonly',
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
            ],
            redirect_uri='http://localhost:3000'  # Replace with your redirect URI
        )
        flow.fetch_token(code=auth_code)
        print("FLOW: ", flow.credentials)
        credentials = flow.credentials
        print("CREDS: ", credentials)
    except: 
        pass

    return {
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'expires_in': credentials.expiry
    }

from google.auth.transport.requests import Request
from django.utils import timezone
from datetime import timedelta

def get_or_refresh_credentials(channel_info):
    if channel_info.token_expiry and channel_info.token_expiry > timezone.now():
        credentials = Credentials(
            token=channel_info.access_token,
            refresh_token=channel_info.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id="119904184627-1ssstt91tkt1lj9lda9e5hb4oi9kiqdo.apps.googleusercontent.com",
            client_secret="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"
        )
    else:
        credentials = Credentials(
            None,
            refresh_token=channel_info.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id="119904184627-1ssstt91tkt1lj9lda9e5hb4oi9kiqdo.apps.googleusercontent.com",
            client_secret="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"
        )
        credentials.refresh(Request())
        channel_info.access_token = credentials.token
        # channel_info.token_expiry = timezone.now() + timedelta(seconds=credentials.expiry)
        print("EXPIRY: ", credentials.expiry)
        expiry_duration = (credentials.expiry - timezone.now()).total_seconds()
        channel_info.token_expiry = timezone.now() + timedelta(seconds=expiry_duration)
        channel_info.save()

    return credentials


# @api_view(["POST"])
# def youtubeAnalytics(request): 
#     username = request.data.get('username')
#     auth_code = request.data.get('auth_code')

#     if not auth_code:
#         return Response({"error": "Authorization code is required"}, status=400)

#     influencerAccount = InfluencerAccount.objects.get(user__username=username)

#     # try:
#     tokens = exchange_auth_code_for_tokens(auth_code)
#     access_token = tokens['access_token']
#     refresh_token = tokens['refresh_token']
#     token_expiry = tokens['expires_in']

#     credentials = Credentials(access_token)
#     youtube = build('youtube', 'v3', credentials=credentials)
#     channel_request = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True)
#     channel_response = channel_request.execute()

#     channel_info = channel_response['items'][0]
#     channel_id = channel_info['id']

#     channel_instance, created = YouTubeChannelInformation.objects.get_or_create(
#         influencer = influencerAccount, 
#         channel_id=channel_id,
#         defaults={
#             "title": channel_info['snippet']['title'],
#             "description": channel_info['snippet']['description'],
#             "custom_url": channel_info['snippet'].get('customUrl'),
#             "published_at": channel_info['snippet']['publishedAt'],
#             "thumbnail_url": channel_info['snippet']['thumbnails']['default']['url'],
#             "view_count": channel_info['statistics']['viewCount'],
#             "subscriber_count": channel_info['statistics']['subscriberCount'],
#             "video_count": channel_info['statistics']['videoCount'],
#             "hidden_subscriber_count": channel_info['statistics']['hiddenSubscriberCount'],
#             "access_token": access_token,
#             "refresh_token": refresh_token,
#             "token_expiry": timezone.now() + timedelta(seconds=3600)
#         }
#     )

#     if not created:
#         credentials = get_or_refresh_credentials(channel_instance)

#     youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
#     start_date = channel_info['snippet']['publishedAt'].split("T")[0]
#     end_date = timezone.now().strftime("%Y-%m-%d")
#     analytics_request = youtube_analytics.reports().query(
#         ids=f'channel=={channel_id}',
#         startDate=start_date,
#         endDate=end_date,
#         metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
#         dimensions='day',
#         sort='day'
#     )
#     analytics_response = analytics_request.execute()

#     for row in analytics_response.get('rows', []):
#         YouTubeChannelAnalytics.objects.create(
#             influencer = influencerAccount,
#             channel_information=channel_instance,
#             date=datetime.strptime(row[0], '%Y-%m-%d'),
#             views=row[1],
#             estimated_minutes_watched=row[2],
#             average_view_duration=row[3],
#             likes=row[4],
#             dislikes=row[5],
#             comments=row[6],
#             shares=row[7],
#         )


#     video_request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, order="date")
#     video_response = video_request.execute()

#     for item in video_response['items']:
#         print("ITEM", item)
#         video_instance, video_created = YouTubeVideoInformation.objects.get_or_create(
#             # influencer = influencerAccount,
#             channel_information=channel_instance,
#             video_id=item['id']['videoId'],
#             defaults={
#                 "title": item['snippet']['title'],
#                 "description": item['snippet']['description'],
#                 "published_at": item['snippet']['publishedAt'],
#                 "thumbnail_url": item['snippet']['thumbnails']['default']['url'],
#             }
#         )

#         if video_created:
#             video_analytics_request = youtube_analytics.reports().query(
#                 ids=f'channel==MINE',
#                 startDate=start_date,
#                 endDate=end_date,
#                 filters=f'video=={item["id"]["videoId"]}',
#                 metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
#                 dimensions='day',
#                 sort='day'
#             )
#             video_analytics_response = video_analytics_request.execute()

#             for row in video_analytics_response.get('rows', []):
#                 YouTubeVideoAnalytics.objects.create(
#                     # influencer = influencerAccount,
#                     video_information=video_instance,
#                     date=datetime.strptime(row[0], '%Y-%m-%d'),
#                     views=row[1],
#                     estimated_minutes_watched=row[2],
#                     average_view_duration=row[3],
#                     likes=row[4],
#                     dislikes=row[5],
#                     comments=row[6],
#                     shares=row[7],
#                 )

#     gender_demographics_request = youtube_analytics.reports().query(
#         ids=f'channel=={channel_id}',
#         startDate=start_date,
#         endDate=end_date,
#         metrics='viewerPercentage',
#         dimensions='gender',
#         sort='gender'
#     )
#     gender_demographics_response = gender_demographics_request.execute()

#     for row in gender_demographics_response.get('rows', []):
#         YouTubeGenderDemographics.objects.create(
#             # influencer = influencerAccount, 
#             channel_information=channel_instance,
#             date=timezone.now(),
#             male_percentage=row[1] if row[0] == 'male' else None,
#             female_percentage=row[1] if row[0] == 'female' else None,
#             unknown_percentage=row[1] if row[0] == 'unknown' else None,
#         )

#     age_demographics_request = youtube_analytics.reports().query(
#         ids=f'channel=={channel_id}',
#         startDate=start_date,
#         endDate=end_date,
#         metrics='viewerPercentage',
#         dimensions='ageGroup',
#         sort='ageGroup'
#     )
#     age_demographics_response = age_demographics_request.execute()

#     for row in age_demographics_response.get('rows', []):
#         YouTubeAgeDemographics.objects.create(
#             # influencer = influencerAccount,
#             channel_information=channel_instance,
#             date=timezone.now(),
#             **{f"age_group_{row[0].replace('-', '_')}": row[1]}
#         )

#     return Response({"message": "Data populated successfully"})

#     # except Exception as e:
#     #     return Response({"error": str(e)}, status=500)




@api_view(["POST"])
def youtubeAnalytics(request): 
    username = request.data.get('username')
    auth_code = request.data.get('auth_code')

    if not auth_code:
        return Response({"error": "Authorization code is required"}, status=400)

    influencerAccount = InfluencerAccount.objects.get(user__username=username)

    try:
        tokens = exchange_auth_code_for_tokens(auth_code)
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        token_expiry = tokens['expires_in']

        credentials = Credentials(access_token)
        youtube = build('youtube', 'v3', credentials=credentials)
        channel_request = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True)
        channel_response = channel_request.execute()

        channel_info = channel_response['items'][0]
        channel_id = channel_info['id']

        channel_instance, created = YouTubeChannelInformation.objects.get_or_create(
            influencer = influencerAccount, 
            channel_id=channel_id,
            defaults={
                "title": channel_info['snippet']['title'],
                "description": channel_info['snippet']['description'],
                "custom_url": channel_info['snippet'].get('customUrl'),
                "published_at": channel_info['snippet']['publishedAt'],
                "thumbnail_url": channel_info['snippet']['thumbnails']['default']['url'],
                "view_count": channel_info['statistics']['viewCount'],
                "subscriber_count": channel_info['statistics']['subscriberCount'],
                "video_count": channel_info['statistics']['videoCount'],
                "hidden_subscriber_count": channel_info['statistics']['hiddenSubscriberCount'],
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_expiry": timezone.now() + timedelta(seconds=3600)
            }
        )

        if not created:
            credentials = get_or_refresh_credentials(channel_instance)

        youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
        start_date = channel_info['snippet']['publishedAt'].split("T")[0]
        end_date = timezone.now().strftime("%Y-%m-%d")
        analytics_request = youtube_analytics.reports().query(
            ids=f'channel=={channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
            dimensions='day',
            sort='day'
        )
        analytics_response = analytics_request.execute()

        for row in analytics_response.get('rows', []):
            YouTubeChannelAnalytics.objects.create(
                influencer = influencerAccount,
                channel_information=channel_instance,
                date=datetime.strptime(row[0], '%Y-%m-%d'),
                views=row[1],
                estimated_minutes_watched=row[2],
                average_view_duration=row[3],
                likes=row[4],
                dislikes=row[5],
                comments=row[6],
                shares=row[7],
            )

        # Get the uploads playlist ID
        channels_response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()
        uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        print("=" * 20)
        print("UPLOADS PLAYLIST ID: ", uploads_playlist_id)

        # Fetch videos from the uploads playlist
        next_page_token = None
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_items_response['items']:
                print("ITEM", item)
                video_id = item['contentDetails']['videoId']
                snippet = item['snippet']
                print("SNIPPET: ", snippet)
                print("VIDEO ID: ", video_id)
                
                video_instance, video_created = YouTubeVideoInformation.objects.get_or_create(
                    channel_information=channel_instance,
                    video_id=video_id,
                    defaults={
                        "title": snippet['title'],
                        "description": snippet['description'],
                        "published_at": snippet['publishedAt'],
                        "thumbnail_url": snippet['thumbnails']['default']['url'],
                    }
                )

                if video_created:
                    video_analytics_request = youtube_analytics.reports().query(
                        ids=f'channel==MINE',
                        startDate=start_date,
                        endDate=end_date,
                        filters=f'video=={video_id}',
                        metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
                        dimensions='day',
                        sort='day'
                    )
                    video_analytics_response = video_analytics_request.execute()
                    print("END DATE: ", end_date)
                    print("VIDEO ANALYTICS RESPONSE: ", video_analytics_response)

                    for row in video_analytics_response.get('rows', []):
                        YouTubeVideoAnalytics.objects.create(
                            video_information=video_instance,
                            date=datetime.strptime(row[0], '%Y-%m-%d'),
                            views=row[1],
                            estimated_minutes_watched=row[2],
                            average_view_duration=row[3],
                            likes=row[4],
                            dislikes=row[5],
                            comments=row[6],
                            shares=row[7],
                        )

            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break
        
        print("=" * 20)
        gender_demographics_request = youtube_analytics.reports().query(
            ids=f'channel=={channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='viewerPercentage',
            dimensions='gender',
            sort='gender'
        )
        gender_demographics_response = gender_demographics_request.execute()
        print("*"*40)
        print("GENDER DEMOGRAPHICS RESPONSE: ", gender_demographics_response)

        for row in gender_demographics_response.get('rows', []):
            print("ROW: ", row)
            YouTubeGenderDemographics.objects.create(
                channel_information=channel_instance,
                date=timezone.now(),
                male_percentage=row[1] if row[0] == 'male' else None,
                female_percentage=row[1] if row[0] == 'female' else None,
                unknown_percentage=row[1] if row[0] == 'unknown' else None,
            )
        print("*"*40)
        age_demographics_request = youtube_analytics.reports().query(
            ids=f'channel=={channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='viewerPercentage',
            dimensions='ageGroup',
            sort='ageGroup'
        )
        age_demographics_response = age_demographics_request.execute()

        for row in age_demographics_response.get('rows', []):
            YouTubeAgeDemographics.objects.create(
                channel_information=channel_instance,
                date=timezone.now(),
                **{f"age_group_{row[0].replace('-', '_')}": row[1]}
            )

        return Response({"message": "Data populated successfully"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)








@api_view(["GET"])
def getYoutubeAnalytics(request):
    # username = request.GET.get("username")
    channel_id = request.GET.get("channel_id")

    # Fetch the InfluencerAccount based on the username
    # try:
    #     influencer = InfluencerAccount.objects.get(user__username=username)
    # except InfluencerAccount.DoesNotExist:
    #     return JsonResponse({"error": "Influencer not found"}, status=404)

    # Retrieve related YouTube data
    channel_info = YouTubeChannelInformation.objects.filter(channel_id=channel_id).first()
    channel_analytics = YouTubeChannelAnalytics.objects.filter(channel_information=channel_info)
    video_info = YouTubeVideoInformation.objects.filter(channel_information=channel_info)
    video_analytics = YouTubeVideoAnalytics.objects.filter(video_information__in=video_info)
    gender_demographics = YouTubeGenderDemographics.objects.filter(channel_information=channel_info)
    age_demographics = YouTubeAgeDemographics.objects.filter(channel_information=channel_info)
    geographic_demographics = YouTubeGeographicDemographics.objects.filter(channel_information=channel_info)

    # Serialize the data
    data = {
        "channel_info": serializers.YouTubeChannelInformationSerializer(channel_info).data if channel_info else None,
        "channel_analytics": serializers.YouTubeChannelAnalyticsSerializer(channel_analytics, many=True).data,
        "video_info": serializers.YouTubeVideoInformationSerializer(video_info, many=True).data,
        "video_analytics": serializers.YouTubeVideoAnalyticsSerializer(video_analytics, many=True).data,
        "gender_demographics": serializers.YouTubeGenderDemographicsSerializer(gender_demographics, many=True).data,
        "age_demographics": serializers.YouTubeAgeDemographicsSerializer(age_demographics, many=True).data,
        "geographic_demographics": serializers.YouTubeGeographicDemographicsSerializer(geographic_demographics, many=True).data,
    }

    return Response(data)

@api_view(["GET"])
def getYoutubeChannelInformation(request):
    # username = request.GET.get("username")
    channel_id = request.GET.get("channel_id")
    # # Fetch the InfluencerAccount based on the username
    # try:
    #     influencer = InfluencerAccount.objects.get(user__username=username)
    # except InfluencerAccount.DoesNotExist:
    #     return JsonResponse({"error": "Influencer not found"}, status=404)

    # Retrieve related YouTube data
    channel_info = YouTubeChannelInformation.objects.filter(channel_id=channel_id)

    # Serialize the data
    data = {
        "channel_info": serializers.YouTubeChannelInformationSerializer(channel_info, many=True).data if channel_info else None,
    }

    return Response(data)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def addYoutubeService(request):
    serializer = serializers.YoutubeServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getYoutubeService(request):
    youtubeChannelInformation = YouTubeChannelInformation.objects.get(channel_id=request.GET.get("channel_id"))
    youtubeServices = models.YoutubeService.objects.filter(channel_information=youtubeChannelInformation)
    serializer = serializers.YoutubeServiceSerializer(youtubeServices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def YoutubeFilterView(request):
    # queryset = filter_influencers(location="Philadelphia", followers=100)
    name = None
    username = None
    followers = None
    price = None
    location = None
    if request.GET.get("name") != "" or request.GET.get("name") != None:
        name = request.GET.get("name")
    if request.GET.get("username") != "" or request.GET.get("username") != None:
        username = request.GET.get("username")
    if request.GET.get("followers") != "" or request.GET.get("followers") != None:
        followers = request.GET.get("followers")
    if request.GET.get("price") != "" or request.GET.get("price") != None:
        price = request.GET.get("price")
    if request.GET.get("location") != "" or request.GET.get("location") != None:
        location = request.GET.get("location", "")
        location = [loc.strip() for loc in location.split(",") if loc.strip()]
    
    queryset = filterYoutubeInfluencers(name, username, followers, price, location)

    
    print("Name: ", name)
    print("Username: ", username)
    print("Followers: ", followers)
    print("Price: ", price)
    print("Location: ", location)
        

    response = []
    responseDict = {}
    for influencer in queryset:
        responseDict["youtube_channel_information"] = model_to_dict(influencer)
        youtubeGeographicDemographics = YouTubeGeographicDemographics.objects.filter(channel_information=influencer).order_by("-date", "-percentage").first()
        if youtubeGeographicDemographics:
            responseDict["youtube_geographic_demographics"] = model_to_dict(youtubeGeographicDemographics)

        # Using annotation to get the lowest price directly from the database
        lowest_price = (
            models.YoutubeServicePricing.objects.filter(service__channel_information=influencer)
            .aggregate(lowest_price=Min("price"))
            .get("lowest_price")
        )
        
        responseDict["lowest_price"] = lowest_price

        response.append(responseDict)
        responseDict = {}

    return JsonResponse(response, safe=False)


def filterYoutubeInfluencers(
    name=None, username=None, followers=None, price=None, location=None
):
    # queryset = YouTubeChannelInformation.objects.all().order_by("channel_id", "-date").distinct("channel_id")
    # Create a subquery to get the latest date per channel_id
    latest_entries = YouTubeChannelInformation.objects.filter(
        channel_id=OuterRef('channel_id')
    ).order_by('-date').values('id')[:1]

    # Start with a base queryset and annotate it with the subquery for filtering
    queryset = YouTubeChannelInformation.objects.filter(
        id__in=Subquery(latest_entries)
    )


    # Filter by name from User model
    if name:
        # queryset = queryset.filter(influencer__user__name__icontains=name)
        queryset = queryset.filter(influencer__user__name__icontains=name)

    # Filter by username from 
    if username: 
        queryset = queryset.filter(custom_url__icontains=username)
    
    # Filter by followers from 
    if followers:
        queryset = queryset.filter(subscriber_count__gte=followers)

    # Filter by price from YoutubeServicePricing
    if price and int(price) > 0:
        queryset = queryset.filter(youtubeservice__youtube_pricings__price__lte=price).distinct()

    # Filter by Audience Location (City or Country)
    if location and len(location) > 0:
        queryset = queryset.filter(youtubegeographicdemographics__country__in=location)
    
    queryset = queryset.order_by("channel_id", "-date")

    return queryset

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getYoutubeRequests(request):
    requests = models.YoutubeRequests.objects.filter(influencer__user__username=request.GET.get("username")).order_by("-request_date")
    serializer = serializers.YoutubeRequestsSerializer(requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def sendYoutubeRequests(request):
    serializer = serializers.YoutubeRequestsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def updateYoutubeRequestState(request):
    requests = models.YoutubeRequests.objects.get(id=request.data.get("request_id"))
    requests.state = request.data.get("state")
    requests.save()
    return Response(status=status.HTTP_200_OK)


# @api_view(["POST"])
# def addTikTokAccount(request): 
#     serializer = serializers.TikTokAccountSerializer(data=request.data)
#     if serializer.is_valid(): 
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# def addTikTokInformation(request): 
#     serializer = serializers.TikTokAccountInformationSerializer(data=request.data)
#     if serializer.is_valid(): 
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def getTikTokAccountData(request): 
#     user = User.objects.get(username=request.GET.get("username"))
#     influencerAccount = InfluencerAccount.objects.get(user=user)
#     tiktokAccounts = TikTokAccount.objects.filter(tiktok_account=influencerAccount)
#     data = []
#     for account in tiktokAccounts: 
#         print("Accounts: ", account)
#         tiktokInfo = TikTokAccountInformation.objects.filter(tiktok_account=account)
#         print("=============>", tiktokInfo.values())
#         account_data = {
#             "id": tiktokInfo.values()[0]["tiktok_account_id"],
#             "information": {
#                 "tiktok_unique_id": tiktokInfo.values()[0]["tiktok_unique_id"],
#                 "tiktok_sec_uid": tiktokInfo.values()[0]["tiktok_sec_uid"],
#                 "tiktok_nickname": tiktokInfo.values()[0]["tiktok_nickname"],
#                 "tiktok_avatar": tiktokInfo.values()[0]["tiktok_avatar"],
#                 "tiktok_signature": tiktokInfo.values()[0]["tiktok_signature"],
#                 "tiktok_digg_count": tiktokInfo.values()[0]["tiktok_digg_count"],
#                 "tiktok_follower_count": tiktokInfo.values()[0]["tiktok_follower_count"],
#                 "tiktok_following_count": tiktokInfo.values()[0]["tiktok_following_count"],
#                 "tiktok_friend_count": tiktokInfo.values()[0]["tiktok_friend_count"],
#                 "tiktok_heart": tiktokInfo.values()[0]["tiktok_heart"],
#                 "tiktok_video_count": tiktokInfo.values()[0]["tiktok_video_count"],
#                 "tiktok_verified": tiktokInfo.values()[0]["tiktok_verified"],
#             }
#         }
#         data.append(account_data)

#     return JsonResponse({"tiktok_accounts": data}, status=200)


@api_view(["GET"])
def getCreatePhylloUser(request):
    user = User.objects.get(username=request.GET.get("username"))
    influencerAccount = InfluencerAccount.objects.get(user=user)
    phylloAccount = models.PhylloAccount.objects.filter(phyllo_account=influencerAccount)

    if phylloAccount.exists():
        try: 
            phylloAccount = phylloAccount.first()
            phylloSDKToken = models.PhylloSDKToken.objects.filter(phyllo_account=phylloAccount)
            if phylloSDKToken.first().phyllo_expires_at > datetime.now(timezone.utc): 
                account_data = {
                    "id": phylloAccount.phyllo_id,
                    "external_id": phylloAccount.phyllo_external_id,
                    "name": phylloAccount.phyllo_name,
                    "sdk_token": phylloSDKToken.first().phyllo_sdk_token
                }
                return Response(account_data, status=200)
            else: 
                url = "https://api.staging.insightiq.ai/v1/sdk-tokens"

                credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()

                payload = {
                    "user_id": phylloAccount.phyllo_id,
                    "products": ["IDENTITY", "IDENTITY.AUDIENCE", "ENGAGEMENT", "ENGAGEMENT.AUDIENCE", "INCOME", "PUBLISH.CONTENT", "ACTIVITY"]
                }
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Basic {encoded_credentials}"
                }

                response = requests.post(url, json=payload, headers=headers)
                phylloSDKToken.first().phyllo_sdk_token = response.json()["sdk_token"]
                phylloSDKToken.first().phyllo_expires_at = datetime.fromisoformat(response.json()["expires_at"])
                phylloSDKToken.first().save()

                account_data = {
                    "id": phylloAccount.phyllo_id,
                    "external_id": phylloAccount.phyllo_external_id,
                    "name": phylloAccount.phyllo_name,
                    "sdk_token": phylloSDKToken.first().phyllo_sdk_token
                }
                return Response(account_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    else:        
        try:  
            url = "https://api.staging.insightiq.ai/v1/users"
            credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            payload = {
                "name": request.GET.get("username"),
                "external_id": User.objects.get(username=request.GET.get("username")).id
            }

            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)
            print("="*10)
            print(response.json())
            print(response.json()["name"])
            print("="*10)
            phylloAccount = models.PhylloAccount(phyllo_account=influencerAccount, 
                                                phyllo_name=response.json()["name"],
                                                phyllo_external_id=response.json()["external_id"],
                                                phyllo_id=response.json()["id"],
                                                phyllo_status=response.json()["status"],
                                                phyllo_created_at=datetime.fromisoformat(response.json()["created_at"]),
                                                phyllo_updated_at=datetime.fromisoformat(response.json()["updated_at"]))
            phylloAccount.save() 


            url = "https://api.staging.insightiq.ai/v1/sdk-tokens"

            payload = {
                "user_id": phylloAccount.phyllo_id,
                "products": ["IDENTITY", "IDENTITY.AUDIENCE", "ENGAGEMENT", "ENGAGEMENT.AUDIENCE", "INCOME", "PUBLISH.CONTENT", "ACTIVITY"]
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_credentials}"
            }

            response = requests.post(url, json=payload, headers=headers)

            phylloSDKToken = models.PhylloSDKToken(phyllo_account=phylloAccount, 
                                  phyllo_sdk_token=response.json()["sdk_token"],
                                  phyllo_expires_at=datetime.fromisoformat(response.json()["expires_at"]))
            phylloSDKToken.save()

            account_data = {
                "id": phylloAccount.phyllo_id,
                "external_id": phylloAccount.phyllo_external_id,
                "name": phylloAccount.phyllo_name,
                "sdk_token": phylloSDKToken.phyllo_sdk_token
            }

            return Response(account_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def getPhylloSDK(request): 
    pass 

@api_view(["GET"])
def savePhylloAccount(request):
    user = User.objects.get(username=request.GET.get("username"))
    influencerAccount = InfluencerAccount.objects.get(user=user)
    phylloAccount= models.PhylloAccount.objects.filter(phyllo_account=influencerAccount)
    if phylloAccount.exists():
        phylloAccount = phylloAccount.first()
        phylloAddedAccounts = models.PhylloAddedAccounts(phyllo_account=phylloAccount, 
                                                         phyllo_accountid=request.GET.get("account_id"),
                                                         phyllo_work_platform_id=request.GET.get("workplatform_id"),
                                                         phyllo_user_id=request.GET.get("user_id"))
        phylloAddedAccounts.save()
        return Response({"status": "success"}, status=200)
    else:
        return Response({"error": "Account Connection Failed"}, status=404)
    
@api_view(["GET"])
def getPhylloContentData(request):
    # Fetch all data and order by published_at
    content_data = models.PhylloContentData.objects.filter(phyllo_accountid=request.GET.get("account_id")).order_by('phyllo_published_at')
    
    # Organize the data into the desired format
    response_data = {
        "work_platform_name": content_data.first().phyllo_work_platform_name if content_data.exists() else "",
        "title": [item.phyllo_title for item in content_data],
        "format": [item.phyllo_format for item in content_data],
        "type": [item.phyllo_type for item in content_data],
        "url": [item.phyllo_url for item in content_data],
        "media_url": [item.phyllo_media_url for item in content_data],
        "duration": [item.phyllo_duration for item in content_data],
        "description": [item.phyllo_description for item in content_data],
        "visibility": [item.phyllo_visibility for item in content_data],
        "thumbnail_url": [item.phyllo_thumbnail_url for item in content_data],
        "published_at": [item.phyllo_published_at for item in content_data],
        "created_at": [item.phyllo_created_at for item in content_data],
        "updated_at": [item.phyllo_updated_at for item in content_data],
        "content_id": [item.phyllo_contentid for item in content_data],
        "like_count": [item.phyllo_engagement_like_count for item in content_data],
        "dislike_count": [item.phyllo_engagement_dislike_count for item in content_data],
        "comment_count": [item.phyllo_engagement_comment_count for item in content_data],
        "impression_organic_count": [item.phyllo_engagement_impression_organic_count for item in content_data],
        "reach_organic_count": [item.phyllo_engagement_reach_organic_count for item in content_data],
        "save_count": [item.phyllo_engagement_save_count for item in content_data],
        "view_count": [item.phyllo_engagement_view_count for item in content_data],
        "watch_time_in_hours": [item.phyllo_engagement_watch_time_in_hours for item in content_data],
        "share_count": [item.phyllo_engagement_share_count for item in content_data],
        "impression_paid_count": [item.phyllo_engagement_impression_paid_count for item in content_data],
        "reach_paid_count": [item.phyllo_engagement_reach_paid_count for item in content_data],
        "sponsored": [item.phyllo_sponsored for item in content_data],
        "collaboration": [item.phyllo_collaboration for item in content_data],
    }

    # Return as JSON response
    return Response(response_data, status=200)

@api_view(["GET"])
def getPhylloContentDataDaily(request):
    # Filter data by account_id
    filtered_data = models.PhylloContentData.objects.filter(phyllo_accountid=request.GET.get("account_id"))

    # Aggregate data grouped by `published_at` date
    aggregated_data = (
        filtered_data.annotate(published_date=TruncDate('phyllo_published_at'))
        .values('published_date')
        .annotate(
            like_count=Sum('phyllo_engagement_like_count'),
            dislike_count=Sum('phyllo_engagement_dislike_count'),
            comment_count=Sum('phyllo_engagement_comment_count'),
            impression_organic_count=Sum('phyllo_engagement_impression_organic_count'),
            reach_organic_count=Sum('phyllo_engagement_reach_organic_count'),
            save_count=Sum('phyllo_engagement_save_count'),
            view_count=Sum('phyllo_engagement_view_count'),
            watch_time_in_hours=Sum('phyllo_engagement_watch_time_in_hours'),
            share_count=Sum('phyllo_engagement_share_count'),
            impression_paid_count=Sum('phyllo_engagement_impression_paid_count'),
            reach_paid_count=Sum('phyllo_engagement_reach_paid_count'),
            sponsored=Sum('phyllo_sponsored'),
            collaboration=Sum('phyllo_collaboration')
        )
        .order_by('published_date')
    )

    # Extract the fields and organize into lists for the response
    response_data = {
        "published_at": [entry['published_date'] for entry in aggregated_data],
        "like_count": [entry['like_count'] for entry in aggregated_data],
        "dislike_count": [entry['dislike_count'] for entry in aggregated_data],
        "comment_count": [entry['comment_count'] for entry in aggregated_data],
        "impression_organic_count": [entry['impression_organic_count'] for entry in aggregated_data],
        "reach_organic_count": [entry['reach_organic_count'] for entry in aggregated_data],
        "save_count": [entry['save_count'] for entry in aggregated_data],
        "view_count": [entry['view_count'] for entry in aggregated_data],
        "watch_time_in_hours": [entry['watch_time_in_hours'] for entry in aggregated_data],
        "share_count": [entry['share_count'] for entry in aggregated_data],
        "impression_paid_count": [entry['impression_paid_count'] for entry in aggregated_data],
        "reach_paid_count": [entry['reach_paid_count'] for entry in aggregated_data],
        "sponsored": [entry['sponsored'] for entry in aggregated_data],
        "collaboration": [entry['collaboration'] for entry in aggregated_data],
    }

    # Return as JSON response
    return Response(response_data, status=200)

@api_view(["GET"])
def getPhylloAudienceDemographicsData(request):
    latest_demo = models.PhylloAudienceDemographics.objects.filter(
        phyllo_account__phyllo_accountid=request.GET.get("account_id")
    ).order_by('-timestamp').first()
    
    if not latest_demo:
        return Response({'error': 'No audience demographics found for the specified account'}, status=404)

    # Construct the JSON response
    response = {
        "gender": {
            "male": latest_demo.phyllo_gender_demographics_male,
            "female": latest_demo.phyllo_gender_demographics_female,
            "other": latest_demo.phyllo_gender_demographics_other
        },
        "age": {
            "13-17": latest_demo.phyllo_age_13_17,
            "18-24": latest_demo.phyllo_age_18_24,
            "25-32": latest_demo.phyllo_age_25_32,
            "33-39": latest_demo.phyllo_age_33_39,
            "40-49": latest_demo.phyllo_age_40_49,
            "50-59": latest_demo.phyllo_age_50_59,
            "60+": latest_demo.phyllo_age_60_plus,
        },
        "country": [
            {
                "country_code": country.country_code,
                "percentage": country.percentage
            } for country in latest_demo.country_demographics.all()
        ],
        "city": [
            {
                "city": city.city,
                "percentage": city.percentage
            } for city in latest_demo.city_demographics.all()
        ]
    }

    return Response(response, status=200)

@api_view(["GET"])
def filterInfluencerProfiles(request):
    queryset = models.PhylloAccountProfile.objects.all()
    filterset = filters.PhylloAccountProfileFilter(request.GET, queryset=queryset)

    if filterset.is_valid():
        queryset = filterset.qs  # Apply filtering

    # Search Functionality
    search_query = request.GET.get('search', None)
    if search_query:
        queryset = queryset.filter(Q(phyllo_user_name__icontains=search_query) | Q(phyllo_category__icontains=search_query))

    # Sorting
    ordering = request.GET.get('ordering', None)
    if ordering:
        queryset = queryset.order_by(ordering)

    serializer = serializers.PhylloAccountProfileSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getPhylloAddedAccounts(request):
    try: 
        phylloAddedAccounts = models.PhylloAddedAccounts.objects.filter(phyllo_account__phyllo_account__user__username=request.GET.get("username"))
        print(phylloAddedAccounts)
        response_data = []
        for addedAccount in phylloAddedAccounts: 
            addedAccountSerializer = serializers.PhylloAddedAccountsSerializer(addedAccount)
            phylloAccountProfile = models.PhylloAccountProfile.objects.filter(phyllo_account=addedAccount)
            phylloAccountProfileSerializer = serializers.PhylloAccountProfileSerializer(phylloAccountProfile[0])
            response_data.append({
                "added_account": addedAccountSerializer.data,
                "profile": phylloAccountProfileSerializer.data
            })
        
        return Response(response_data, status=200)

    except Exception as e: 
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def addCampaign(request): 
    serializer = serializers.CampaignSerializer(data=request.data)
    if serializer.is_valid(): 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getCampaigns(request): 
    try:
        user = User.objects.get(username=request.GET.get("username"))
        campaigns = models.Campaign.objects.filter(user=user)
        serializer = serializers.CampaignSerializer(campaigns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def getCampaingsForInfluencers(request): 
    try: 
        response_data = []
        accepted_data = []
        pending_data = []
        influencerCampaigns = models.CampaignInfluencer.objects.filter(influencer__phyllo_accountid=request.GET.get("account_id"), status="ADDED")   
        for influencerCampaign in influencerCampaigns:
            campaign = influencerCampaign.campaign
            businessAccount = models.BusinessAccount.objects.get(user=campaign.user)
            campaign = serializers.CampaignSerializer(campaign).data
            campaignInfluencer = serializers.CampaignInfluencerSerializer(influencerCampaign).data
            

            accepted_data.append({
                "campaign": campaign, 
                "campaign_influencer": campaignInfluencer,
                "company_name": businessAccount.company_name,
                "service_type": influencerCampaign.service.service_type,
                "pricing_method": influencerCampaign.service.pricing_method,    
                "final_price": influencerCampaign.final_price,
                "content_provider": influencerCampaign.content_provider,
                "amount": influencerCampaign.amount
            })
        
        influencerCampaigns = models.CampaignInfluencer.objects.filter(influencer__phyllo_accountid=request.GET.get("account_id"), status="PENDING")   
        for influencerCampaign in influencerCampaigns:
            campaign = influencerCampaign.campaign
            businessAccount = models.BusinessAccount.objects.get(user=campaign.user)
            campaign = serializers.CampaignSerializer(campaign).data
            campaignInfluencer = serializers.CampaignInfluencerSerializer(influencerCampaign).data
            

            pending_data.append({
                "campaign": campaign, 
                "campaign_influencer": campaignInfluencer,
                "company_name": businessAccount.company_name,
                "service_type": influencerCampaign.service.service_type,
                "pricing_method": influencerCampaign.service.pricing_method,    
                "final_price": influencerCampaign.final_price,
                "content_provider": influencerCampaign.content_provider,
                "amount": influencerCampaign.amount
            })

        return Response({"accepted": accepted_data, "pending_data": pending_data}, status=200)

    except Exception as ex: 
        return Response({"error": str(ex)}, status=500)

@api_view(["GET"])
def addInfluencerToCampaign(request):
    try: 
        campaign = models.Campaign.objects.get(id=request.GET.get("campaign_id"))
        phylloAddedAccount = models.PhylloAddedAccounts.objects.get(phyllo_accountid=request.GET.get("account_id"))
        print(request.GET.get("service_type"))
        print(request.GET.get("pricing_method"))

        influencerService = models.InfluencerService.objects.get(account=phylloAddedAccount, service_type=request.GET.get("service_type"), pricing_method=request.GET.get("pricing_method"), content_provider=request.GET.get("content_provider"))

        if not models.CampaignInfluencer.objects.filter(campaign=campaign, influencer=phylloAddedAccount).exists(): 
            campaignInfluencer = models.CampaignInfluencer(
                campaign=campaign,
                influencer=phylloAddedAccount, 
                service=influencerService,
                amount=request.GET.get("amount"),
                final_price=influencerService.price,
                content_provider=request.GET.get("content_provider"),
                num_posts=request.GET.get("num_posts"),
            )
            campaignInfluencer.save()
            return Response({"status": "success"}, status=200)
        return Response({"error": "Influencer already added to campaign"}, status=400)
    except Exception as e: 
        print(e)
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def updateInfluencerCampaignAddStatus(request): 
    try: 
        campaign = models.Campaign.objects.get(id=request.GET.get("campaign_id"))   
        phylloAddedAccount = models.PhylloAddedAccounts.objects.get(phyllo_accountid=request.GET.get("account_id"))
        campaignInfluencer = models.CampaignInfluencer.objects.get(campaign=campaign, influencer=phylloAddedAccount)
        campaignInfluencer.status = "ADDED"
        campaignInfluencer.save()
        return Response({"status": "success"}, status=200)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def getInfluencersInCampaign(request): 
    try:
        campaign = models.Campaign.objects.get(id=request.GET.get("campaign_id"))
        company_name = BusinessAccount.objects.get(user__username=request.GET.get("username")).company_name
        campaignInfluencers = models.CampaignInfluencer.objects.filter(campaign=campaign)

        accepted = []
        pending = []

        for campaign_influencer in campaignInfluencers:
            latest_phyllo_profile = models.PhylloAccountProfile.objects.filter(
                phyllo_account=campaign_influencer.influencer
            ).order_by("-timestamp").first()  # Get the latest entry
            
            campaign_influencer_data = serializers.CampaignInfluencerSerializer(campaign_influencer).data
            phyllo_profile_data = serializers.PhylloAccountProfileSerializer(latest_phyllo_profile).data if latest_phyllo_profile else None


            data = {
                "campaign_influencer": campaign_influencer_data,
                "latest_phyllo_profile": phyllo_profile_data,
                "company_name": company_name
            }

            if campaign_influencer.status == "ADDED":
                accepted.append(data)
            elif campaign_influencer.status == "PENDING":
                pending.append(data)

        return Response({"accepted": accepted, "pending": pending}, status=status.HTTP_200_OK)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)


@api_view(["GET", "POST"])
def addInfluencerService(request): 
    try: 
        data = request.data
        phylloAddedAccount = models.PhylloAddedAccounts.objects.get(phyllo_accountid=request.GET.get("account_id"))
        print("DATA: ", data)
        for entry in data: 
            print("ENTRY: ", entry)

            # influencerService = models.InfluencerService(
            #     account = phylloAddedAccount,
            #     service_type = entry["service_type"],
            #     pricing_method = entry["pricing_method"],
            #     pricing_method_activated = entry["pricing_method_activated"],
            #     price = entry["price"],
            #     content_provider=entry["content_provider"],
            #     # content_provider_business = entry["content_provider_business"],
            #     # content_provider_influencer = entry["content_provider_influencer"],
            # )
            # influencerService.save()
            influencerService, created = models.InfluencerService.objects.update_or_create(
                account=phylloAddedAccount,
                service_type=entry["service_type"],
                content_provider=entry["content_provider"],  # Include this field to ensure uniqueness
                defaults={
                    "pricing_method": entry["pricing_method"],
                    "pricing_method_activated": entry["pricing_method_activated"],
                    "price": entry["price"],
                    # "content_provider_business": entry["content_provider_business"],
                    # "content_provider_influencer": entry["content_provider_influencer"],
                }
            )
        return Response({"status": "success"}, status=200)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def getInfluencerService(request):
    try: 
        phylloAddedAccount = models.PhylloAddedAccounts.objects.get(phyllo_accountid=request.GET.get("account_id"))
        influencerServices = models.InfluencerService.objects.filter(account=phylloAddedAccount)
        serializer = serializers.InfluencerServiceSerializer(influencerServices, many=True)
        return Response(serializer.data, status=200)
    except Exception as ex: 
        return Response({"error": str(ex)}, status=500)

@api_view(["GET"])
def acceptInfluencerCampaign(request): 
    try: 
        campaignInfluencer = models.CampaignInfluencer.objects.get(campaign__id=request.GET.get("campaign_id"), influencer__phyllo_accountid=request.GET.get("account_id"))
        campaignInfluencer.status = "ADDED"
        

        phylloAddedAccount = models.PhylloAddedAccounts.objects.get(phyllo_accountid=request.GET.get("account_id"))
        businessAccount = models.BusinessAccount.objects.get(user=campaignInfluencer.campaign.user)
        contract = models.Contract(campaign_influencer=campaignInfluencer, phyllo_added_account=phylloAddedAccount, business=businessAccount)
        contract.save()
        contractVersion = models.ContractVersion(
            contract=contract,
            contract_version=1,
            contract_text="",
            owner=campaignInfluencer.campaign.user,
        )
        


        chatModel = ChatModel(
            user1 = campaignInfluencer.campaign.user,
            user2 = phylloAddedAccount.phyllo_account.phyllo_account.user,
            room_name = f"{campaignInfluencer.campaign.user.username}-{phylloAddedAccount.phyllo_account.phyllo_account.user.username}"
        )
        contractVersion.save()
        campaignInfluencer.save()
        chatModel.save()

        return Response({"status": "success"}, status=200)
    except Exception as ex: 
        return Response({"error": str(ex)}, status=500)

@api_view(["GET"])
def declineInfluencerCampaign(request): 
    campaignInfluencer = models.CampaignInfluencer.objects.get(campaign__id=request.GET.get("campaign_id"), influencer__phyllo_accountid=request.GET.get("account_id"))
    campaignInfluencer.delete()

@api_view(["GET"])
def schedulePost(request): 
    try: 
        # Get the related PhylloAddedAccounts instance
        phyllo_account = models.PhylloAddedAccounts.objects.get(phyllo_accountid=request.GET.get("account_id"))
        campaignInfluencers=models.CampaignInfluencer.objects.get(campaign__id=request.GET.get("campaign_id"), influencer__phyllo_accountid=request.GET.get("account_id"), timestamp=request.GET.get("timestamp"))
        if BusinessAccount.objects.filter(user__username=request.GET.get("username")).exists():
            # Create a new PhylloScheduledPost instance
            phylloScheduledPost = models.PhylloScheduledPost(
                phyllo_account=phyllo_account,  # Pass the instance, not a lookup string
                title=request.GET.get("caption"),
                media_source_media_url=request.GET.get("media_url"),
                scheduled_time=request.GET.get("scheduled_time"),
                business_accepted=True,
                campaign_influencers=campaignInfluencers,
                campaign_files=models.CampaignFiles.objects.get(id=request.GET.get("file_id"))
            )
            phylloScheduledPost.save()
        elif InfluencerAccount.objects.filter(user__username=request.GET.get("username")).exists():
            # Create a new PhylloScheduledPost instance
            phylloScheduledPost = models.PhylloScheduledPost(
                phyllo_account=phyllo_account,  # Pass the instance, not a lookup string
                title=request.GET.get("caption"),
                media_source_media_url=request.GET.get("media_url"),
                scheduled_time=request.GET.get("scheduled_time"),
                influencer_accepted=True,
                campaign_influencers=campaignInfluencers,
                campaign_files=models.CampaignFiles.objects.get(id=request.GET.get("file_id"))               
            )

        
            phylloScheduledPost.save()                                                    

        return Response({"status": "success"}, status=200)
    except models.PhylloAddedAccounts.DoesNotExist:
        return Response({"status": "PhylloAddedAccounts not found"}, status=404)
    except Exception as e: 
        return Response({"status": str(e)}, status=400)

@api_view(['POST'])
def uploadCampaignFile(request):
    try: 
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)
        
        file_path = default_storage.save(file.name, file)
        file_url = f"https://marketingos.nyc3.cdn.digitaloceanspaces.com/{settings.AWS_STORAGE_BUCKET_NAME}/{file_path}"


        campaign = models.Campaign.objects.get(id=request.GET.get("campaign"))
        campaignFiles = models.CampaignFiles(campaign=campaign,
                                            file_name=file.name,
                                            file_size=file.size,
                                            file_url=file_url)
        campaignFiles.save()
        

        return Response({'file_url': file_url}, status=200)
    except Exception as e: 
        return Response({'error': str(e)}, status=400)


@api_view(["GET"])
def getCampaignFiles(request):
    try: 
        campaign = models.Campaign.objects.get(id=request.GET.get("campaign"))
        campaignFiles = models.CampaignFiles.objects.filter(campaign=campaign)
        serializer = serializers.CampaignFilesSerializer(campaignFiles, many=True)
        return Response(serializer.data, status=200)

    except Exception as e: 
        return Response({'error': str(e)}, status=400)
    
@api_view(["GET"])
def getCampaignFileScheduledPost(request): 
    try: 
        campaignFiles = models.CampaignFiles.objects.get(id=request.GET.get("file_id"))
        phylloScheduledPost = models.PhylloScheduledPost.objects.get(campaign_files=campaignFiles)
        campaign = models.Campaign.objects.get(id=request.GET.get("campaign_id"))
        campaignInfluencer = models.CampaignInfluencer.objects.get(campaign=campaign, influencer__phyllo_accountid=request.GET.get("account_id"))
        # print(f"campaign files: {campaignFiles} scheduled post: {phylloScheduledPost} campaign: {campaign} campaign influencer: {campaignInfluencer}")
        response_data = {'scheduled_post_id': phylloScheduledPost.id, 'state': None}
        if BusinessAccount.objects.filter(user__username=request.GET.get("username")).exists():
            if campaignInfluencer.content_provider == 'business':
                # print("HERE")
                if phylloScheduledPost.business_accepted == True and phylloScheduledPost.influencer_accepted == False: 
                    response_data['state'] = 'pending'
                elif phylloScheduledPost.business_accepted == True and phylloScheduledPost.influencer_accepted == True:
                    response_data['state'] = 'accepted'
            elif campaignInfluencer.content_provider == 'influencer':
                if phylloScheduledPost.influencer_accepted == True and phylloScheduledPost.business_accepted == False: 
                    response_data['state'] = 'request'
                elif phylloScheduledPost.influencer_accepted == True and phylloScheduledPost.business_accepted == True:
                    response_data['state'] = 'accepted'
        elif InfluencerAccount.objects.filter(user__username=request.GET.get("username")).exists():
            if campaignInfluencer.content_provider == 'business':
                if phylloScheduledPost.business_accepted == True and phylloScheduledPost.influencer_accepted == False: 
                    response_data['state'] = 'request'
                elif phylloScheduledPost.business_accepted == True and phylloScheduledPost.influencer_accepted == True:
                    response_data['state'] = 'accepted'
            elif campaignInfluencer.content_provider == 'influencer':
                if phylloScheduledPost.influencer_accepted == True and phylloScheduledPost.business_accepted == False: 
                    response_data['state'] = 'pending'
                elif phylloScheduledPost.influencer_accepted == True and phylloScheduledPost.business_accepted == True:
                    response_data['state'] = 'accepted'
        return Response(response_data, status=200)

    except Exception as e: 
        return Response({'state': str(e)}, status=400)
    
@api_view(["GET"])
def acceptScheduleRequest(request): 
    try: 
        phylloScheduledPost = models.PhylloScheduledPost.objects.get(id=request.GET.get("scheduled_post_id"))
        if BusinessAccount.objects.filter(user__username=request.GET.get("username")).exists():
            phylloScheduledPost.business_accepted = True
        elif InfluencerAccount.objects.filter(user__username=request.GET.get("username")).exists():
            phylloScheduledPost.influencer_accepted = True
        phylloScheduledPost.save()
        return Response({"status": "success"}, status=200)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)
    
@api_view(["GET"])
def removeScheduled(request): 
    try: 
        phylloScheduledPost = models.PhylloScheduledPost.objects.get(id=request.GET.get("scheduled_post_id"))
        phylloScheduledPost.delete()
        return Response({"status": "success"}, status=200)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)
    
@api_view(["GET"])
def getCampaignDetails(request):
    try: 
        campaign = models.Campaign.objects.get(id=request.GET.get("campaign_id"))
        campaignInfluencers = models.CampaignInfluencer.objects.get(campaign=campaign, influencer__phyllo_accountid=request.GET.get("account_id"))
        campaignInfluencersSerializer = serializers.CampaignInfluencerSerializer(campaignInfluencers)
        return Response(campaignInfluencersSerializer.data, status=200)

    except Exception as e: 
        print("Error: ", e)
        return Response({'error': str(e)}, status=400)
    
@api_view(["GET"])
def markPaymentPaid(request): 
    try: 
        campaignInfluencers = models.CampaignInfluencer.objects.get(campaign__id=request.GET.get("campaign_id"), influencer__phyllo_accountid=request.GET.get("account_id"))
        phylloScheduledPosts = models.PhylloScheduledPost.objects.filter(campaign_influencers=campaignInfluencers)
        for scheduled in phylloScheduledPosts: 
            scheduled.payment_completed=True
            scheduled.save()
        
        return Response({"status": "success"}, status=200)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)

@api_view(["GET", "POST"])
def publishedSuccessWebhook(request): 
    try:
        body = request.body
        data = json.loads(body)
        print("body: ", body)
        print("data: ", data)

        # Refresh Content List 
        url = "https://api.staging.insightiq.ai/v1/social/contents/refresh"
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        payload = {
            "account_id": data["data"]["account_id"]    
        }

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, json=payload, headers=headers)

        # Get contents 
        url = "https://api.staging.insightiq.ai/v1/social/contents?account_id=" + data["data"]["account_id"]
        response = requests.get(url, headers=headers)
        latest_content = response.json()["data"][0]
        latest_content_id = latest_content["id"]
        print("latest content id: ", latest_content_id)
        # Update PhylloScheduledPost entry
        phylloScheduledPost = models.PhylloScheduledPost.objects.get(publish_id=data["data"]["publish_id"])
        phylloScheduledPost.content_id = latest_content_id
        phylloScheduledPost.final_status = "SUCCESS"
        phylloScheduledPost.save()
        
        return Response({"status": "success"}, status=200)

    except Exception as e: 
        return Response({"error": str(e)}, status=500)
    

@api_view(["GET"])
def getPhylloPostedContentData(request):
    try: 
        phylloPostedContentData = models.PhylloPostedContentData.objects.filter(phyllo_scheduled_post__id=request.GET.get("scheduled_post_id")).order_by("timestamp")
        # content_data = models.PhylloContentData.objects.filter(phyllo_accountid=request.GET.get("account_id")).order_by('phyllo_published_at')
    
    # Organize the data into the desired format
        response_data = {
            "work_platform_name": phylloPostedContentData.first().phyllo_work_platform_name if phylloPostedContentData.exists() else "",
            "title": [item.phyllo_title for item in phylloPostedContentData],
            "format": [item.phyllo_format for item in phylloPostedContentData],
            "type": [item.phyllo_type for item in phylloPostedContentData],
            "url": [item.phyllo_url for item in phylloPostedContentData],
            "media_url": [item.phyllo_media_url for item in phylloPostedContentData],
            "duration": [item.phyllo_duration for item in phylloPostedContentData],
            "description": [item.phyllo_description for item in phylloPostedContentData],
            "visibility": [item.phyllo_visibility for item in phylloPostedContentData],
            "thumbnail_url": [item.phyllo_thumbnail_url for item in phylloPostedContentData],
            "published_at": [item.phyllo_published_at for item in phylloPostedContentData],
            "created_at": [item.phyllo_created_at for item in phylloPostedContentData],
            "updated_at": [item.phyllo_updated_at for item in phylloPostedContentData],
            "content_id": [item.phyllo_contentid for item in phylloPostedContentData],
            "like_count": [item.phyllo_engagement_like_count for item in phylloPostedContentData],
            "dislike_count": [item.phyllo_engagement_dislike_count for item in phylloPostedContentData],
            "comment_count": [item.phyllo_engagement_comment_count for item in phylloPostedContentData],
            "impression_organic_count": [item.phyllo_engagement_impression_organic_count for item in phylloPostedContentData],
            "reach_organic_count": [item.phyllo_engagement_reach_organic_count for item in phylloPostedContentData],
            "save_count": [item.phyllo_engagement_save_count for item in phylloPostedContentData],
            "view_count": [item.phyllo_engagement_view_count for item in phylloPostedContentData],
            "watch_time_in_hours": [item.phyllo_engagement_watch_time_in_hours for item in phylloPostedContentData],
            "share_count": [item.phyllo_engagement_share_count for item in phylloPostedContentData],
            "impression_paid_count": [item.phyllo_engagement_impression_paid_count for item in phylloPostedContentData],
            "reach_paid_count": [item.phyllo_engagement_reach_paid_count for item in phylloPostedContentData],
            "sponsored": [item.phyllo_sponsored for item in phylloPostedContentData],
            "collaboration": [item.phyllo_collaboration for item in phylloPostedContentData],
        }

        return Response(response_data, status=200)

    except Exception as e: 
        print("Error: ", e)
        return Response({"error": str(e)}, status=500)
    
@api_view(["GET"])
def getScheduledPosts(request):
    try: 
        campaignFiles = models.CampaignFiles.objects.get(id=request.GET.get("file_id"))
        phylloScheduledPosts = models.PhylloScheduledPost.objects.get(phyllo_account__phyllo_accountid=request.GET.get("account_id"), campaign_files=campaignFiles)
        serializer = serializers.PhylloScheduledPostSerializer(phylloScheduledPosts)
        return Response(serializer.data, status=200)
    except Exception as e: 
        return Response({"error": str(e)}, status=500)