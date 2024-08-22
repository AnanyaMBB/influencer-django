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
    RequestsSerializer,
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
    Requests,
)
from . import models
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
@permission_classes([IsAuthenticated])
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
    influencer_email = contract.influencer.user.email

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
@permission_classes([IsAuthenticated])
def getElementDetails(request):
    # try:
    contract = Contract.objects.get(contract_id=request.GET.get("contract_id"))
    contract_version = ContractVersion.objects.get(
        contract=contract, contract_version=request.GET.get("version_id")
    )
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
        instagram_id=contract.influencerInstagramInformation.instagram_id
    )
    instagramInitialInformation = InstagramInitialInformation.objects.filter(
        influencer_instagram_information=influencerInstagramInformation
    ).latest("date")
    return_data = {
        "company_name": contract.business.company_name,
        "influencer_name": contract.influencer.user.get_full_name(),
        "influencer_username": instagramInitialInformation.username,
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


# @api_view(["POST"])
# def youtubeAnalytics(request): 
#     access_token = request.data.get('access_token')

#     if not access_token:
#         return Response({"error": "Access token is required"}, status=400)

#     try:
#         credentials = Credentials(access_token)

#         # Step 1: Use YouTube Data API to get the authenticated user's channel ID
#         youtube = build('youtube', 'v3', credentials=credentials)
#         channel_request = youtube.channels().list(part="id", mine=True)
#         channel_response = channel_request.execute()
        
#         # Extract the channel ID from the response
#         channel_id = channel_response['items'][0]['id']
#         print(f"Channel ID: {channel_id}")

#         # Step 2: Use YouTube Analytics API to fetch analytics data for the channel
#         youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
#         analytics_request = youtube_analytics.reports().query(
#             ids=f'channel=={channel_id}',  # Use the obtained channel ID
#             startDate='2023-01-01',        # Set the desired start date
#             endDate='2023-12-31',          # Set the desired end date
#             metrics='views,estimatedMinutesWatched,averageViewDuration',  # Metrics to retrieve
#             dimensions='day',              # Breakdown the data by day
#             sort='day'                     # Sort the results by day
#         )

#         # Execute the analytics request
#         analytics_response = analytics_request.execute()
#         print("YouTube Analytics Data: ", analytics_response)

#         return Response(analytics_response)
    
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)


# @api_view(["POST"])
# def youtubeAnalytics(request): 
#     access_token = request.data.get('access_token')

#     if not access_token:
#         return Response({"error": "Access token is required"}, status=400)

#     # try:
#     credentials = Credentials(access_token)

#     # Step 1: Use YouTube Data API to get the authenticated user's channel ID
#     youtube = build('youtube', 'v3', credentials=credentials)
#     channel_request = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True)
#     channel_response = channel_request.execute()

#     # Extract the channel information
#     channel_info = channel_response['items'][0]
#     channel_id = channel_info['id']

#     # Check if the channel already exists in the database
#     channel_instance, created = YouTubeChannelInformation.objects.get_or_create(
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
#         }
#     )

#     # If the channel was just created, populate historical data
#     if created:
#         start_date = channel_info['snippet']['publishedAt'].split("T")[0]  # Assuming the channel's start date
#         end_date = datetime.now().strftime("%Y-%m-%d")

#         # Populate channel analytics
#         youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
#         analytics_request = youtube_analytics.reports().query(
#             ids=f'channel=={channel_id}',
#             startDate=start_date,
#             endDate=end_date,
#             metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
#             dimensions='day',
#             sort='day'
#         )
#         analytics_response = analytics_request.execute()

#         for row in analytics_response.get('rows', []):
#             YouTubeChannelAnalytics.objects.create(
#                 channel_information=channel_instance,
#                 date=datetime.strptime(row[0], '%Y-%m-%d'),
#                 views=row[1],
#                 estimated_minutes_watched=row[2],
#                 average_view_duration=row[3],
#                 likes=row[4],
#                 dislikes=row[5],
#                 comments=row[6],
#                 shares=row[7],
#             )

#         # Populate video information and analytics
#         video_request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, order="date")
#         video_response = video_request.execute()

#         for item in video_response['items']:
#             video_instance, video_created = YouTubeVideoInformation.objects.get_or_create(
#                 channel_information=channel_instance,
#                 video_id=item['id']['videoId'],
#                 defaults={
#                     "title": item['snippet']['title'],
#                     "description": item['snippet']['description'],
#                     "published_at": item['snippet']['publishedAt'],
#                     "thumbnail_url": item['snippet']['thumbnails']['default']['url'],
#                 }
#             )

#             if video_created:
#                 video_analytics_request = youtube_analytics.reports().query(
#                     ids=f'channel==MINE',
#                     startDate=start_date,
#                     endDate=end_date,
#                     filters=f'video=={item["id"]["videoId"]}',
#                     metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
#                     dimensions='day',
#                     sort='day'
#                 )
#                 video_analytics_response = video_analytics_request.execute()

#                 for row in video_analytics_response.get('rows', []):
#                     YouTubeVideoAnalytics.objects.create(
#                         video_information=video_instance,
#                         date=datetime.strptime(row[0], '%Y-%m-%d'),
#                         views=row[1],
#                         estimated_minutes_watched=row[2],
#                         average_view_duration=row[3],
#                         likes=row[4],
#                         dislikes=row[5],
#                         comments=row[6],
#                         shares=row[7],
#                     )

#         # Populate gender demographics
#         gender_demographics_request = youtube_analytics.reports().query(
#             ids=f'channel=={channel_id}',
#             startDate=start_date,
#             endDate=end_date,
#             metrics='viewerPercentage',
#             dimensions='gender',
#             sort='gender'
#         )
#         gender_demographics_response = gender_demographics_request.execute()

#         for row in gender_demographics_response.get('rows', []):
#             YouTubeGenderDemographics.objects.create(
#                 channel_information=channel_instance,
#                 date=datetime.now(),
#                 male_percentage=row[1] if row[0] == 'male' else None,
#                 female_percentage=row[1] if row[0] == 'female' else None,
#                 unknown_percentage=row[1] if row[0] == 'unknown' else None,
#             )

#         # Populate age demographics
#         age_demographics_request = youtube_analytics.reports().query(
#             ids=f'channel=={channel_id}',
#             startDate=start_date,
#             endDate=end_date,
#             metrics='viewerPercentage',
#             dimensions='ageGroup',
#             sort='ageGroup'
#         )
#         age_demographics_response = age_demographics_request.execute()

#         for row in age_demographics_response.get('rows', []):
#             YouTubeAgeDemographics.objects.create(
#                 channel_information=channel_instance,
#                 date=datetime.now(),
#                 **{f"age_group_{row[0].replace('-', '_')}": row[1]}
#             )

#     return Response({"message": "Data populated successfully"})

#     # except Exception as e:
#     #     return Response({"error": str(e)}, status=500)


# @api_view(["POST"])
# def youtubeAnalytics(request): 
#     access_token = request.data.get('access_token')

#     if not access_token:
#         return Response({"error": "Access token is required"}, status=400)

#     # try:
#     credentials = Credentials(access_token)

#     # Step 1: Use YouTube Data API to get the authenticated user's channel ID
#     youtube = build('youtube', 'v3', credentials=credentials)
#     channel_request = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True)
#     channel_response = channel_request.execute()

#     # Extract the channel information
#     channel_info = channel_response['items'][0]
#     channel_id = channel_info['id']

#     # Check if the channel already exists in the database
#     channel_instance, created = YouTubeChannelInformation.objects.get_or_create(
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
#         }
#     )

#     # Populate channel analytics
#     youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
#     start_date = channel_info['snippet']['publishedAt'].split("T")[0]
#     end_date = datetime.now().strftime("%Y-%m-%d")
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

#     # Populate video information and analytics
#     video_request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, order="date")
#     video_response = video_request.execute()

#     for item in video_response['items']:
#         video_instance, video_created = YouTubeVideoInformation.objects.get_or_create(
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

#     # Populate gender demographics
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
#             channel_information=channel_instance,
#             date=datetime.now(),
#             male_percentage=row[1] if row[0] == 'male' else None,
#             female_percentage=row[1] if row[0] == 'female' else None,
#             unknown_percentage=row[1] if row[0] == 'unknown' else None,
#         )

#     # Populate age demographics
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
#             channel_information=channel_instance,
#             date=datetime.now(),
#             **{f"age_group_{row[0].replace('-', '_')}": row[1]}
#         )

#     return Response({"message": "Data populated successfully"})

#     # except Exception as e:
#     #     return Response({"error": str(e)}, status=500)




# def get_or_refresh_credentials(channel_info):
#     if channel_info.token_expiry and channel_info.token_expiry > datetime.now():
#         # Token is still valid
#         credentials = Credentials(
#             token=channel_info.access_token,
#             refresh_token=channel_info.refresh_token,
#             token_uri="https://oauth2.googleapis.com/token",
#             client_id="YOUR_CLIENT_ID",  # Replace with your client_id
#             client_secret="YOUR_CLIENT_SECRET"  # Replace with your client_secret
#         )
#     else:
#         # Token has expired, refresh it
#         credentials = Credentials(
#             None,
#             refresh_token=channel_info.refresh_token,
#             token_uri="https://oauth2.googleapis.com/token",
#             client_id="YOUR_CLIENT_ID",
#             client_secret="YOUR_CLIENT_SECRET"
#         )
#         credentials.refresh(Request())

#         # Update the access token and expiry time in the database
#         channel_info.access_token = credentials.token
#         channel_info.token_expiry = datetime.now() + timedelta(seconds=credentials.expiry)
#         channel_info.save()

#     return credentials

# @api_view(["POST"])
# def youtubeAnalytics(request): 
#     access_token = request.data.get('access_token')
#     refresh_token = request.data.get('refresh_token')
#     print("ACCESS TOKEN: ",access_token)
#     print("REFRESH TOKEN: ",refresh_token)

#     if not access_token or not refresh_token:
#         return Response({"error": "Access token and refresh token are required"}, status=400)

#     # Use the provided access token to fetch the initial channel information
#     credentials = Credentials(access_token)
#     youtube = build('youtube', 'v3', credentials=credentials)
#     channel_request = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True)
#     channel_response = channel_request.execute()

#     # Extract the channel information
#     channel_info = channel_response['items'][0]
#     channel_id = channel_info['id']

#     # Check if the channel already exists in the database
#     channel_instance, created = YouTubeChannelInformation.objects.get_or_create(
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
#             "token_expiry": datetime.now() + timedelta(seconds=3600)  # Set token expiry to 1 hour from now
#         }
#     )

#     # If the channel already existed, make sure to use or refresh the stored credentials
#     if not created:
#         credentials = get_or_refresh_credentials(channel_instance)

#     # Step 2: Use the YouTube Analytics API to fetch and store analytics data
#     youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
#     start_date = channel_info['snippet']['publishedAt'].split("T")[0]
#     end_date = datetime.now().strftime("%Y-%m-%d")
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

#     # Step 3: Populate video information and analytics
#     video_request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, order="date")
#     video_response = video_request.execute()

#     for item in video_response['items']:
#         video_instance, video_created = YouTubeVideoInformation.objects.get_or_create(
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

#     # Step 4: Populate gender demographics
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
#             channel_information=channel_instance,
#             date=datetime.now(),
#             male_percentage=row[1] if row[0] == 'male' else None,
#             female_percentage=row[1] if row[0] == 'female' else None,
#             unknown_percentage=row[1] if row[0] == 'unknown' else None,
#         )

#     # Step 5: Populate age demographics
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
#             channel_information=channel_instance,
#             date=datetime.now(),
#             **{f"age_group_{row[0].replace('-', '_')}": row[1]}
#         )

#     return Response({"message": "Data populated successfully"})




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


@api_view(["POST"])
def youtubeAnalytics(request): 
    username = request.data.get('username')
    auth_code = request.data.get('auth_code')

    if not auth_code:
        return Response({"error": "Authorization code is required"}, status=400)

    influencerAccount = InfluencerAccount.objects.get(user__username=username)

    # try:
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

    video_request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50, order="date")
    video_response = video_request.execute()

    for item in video_response['items']:
        video_instance, video_created = YouTubeVideoInformation.objects.get_or_create(
            influencer = influencerAccount,
            channel_information=channel_instance,
            video_id=item['id']['videoId'],
            defaults={
                "title": item['snippet']['title'],
                "description": item['snippet']['description'],
                "published_at": item['snippet']['publishedAt'],
                "thumbnail_url": item['snippet']['thumbnails']['default']['url'],
            }
        )

        if video_created:
            video_analytics_request = youtube_analytics.reports().query(
                ids=f'channel==MINE',
                startDate=start_date,
                endDate=end_date,
                filters=f'video=={item["id"]["videoId"]}',
                metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
                dimensions='day',
                sort='day'
            )
            video_analytics_response = video_analytics_request.execute()

            for row in video_analytics_response.get('rows', []):
                YouTubeVideoAnalytics.objects.create(
                    influencer = influencerAccount,
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

    gender_demographics_request = youtube_analytics.reports().query(
        ids=f'channel=={channel_id}',
        startDate=start_date,
        endDate=end_date,
        metrics='viewerPercentage',
        dimensions='gender',
        sort='gender'
    )
    gender_demographics_response = gender_demographics_request.execute()

    for row in gender_demographics_response.get('rows', []):
        YouTubeGenderDemographics.objects.create(
            influencer = influencerAccount, 
            channel_information=channel_instance,
            date=timezone.now(),
            male_percentage=row[1] if row[0] == 'male' else None,
            female_percentage=row[1] if row[0] == 'female' else None,
            unknown_percentage=row[1] if row[0] == 'unknown' else None,
        )

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
            influencer = influencerAccount,
            channel_information=channel_instance,
            date=timezone.now(),
            **{f"age_group_{row[0].replace('-', '_')}": row[1]}
        )

    return Response({"message": "Data populated successfully"})

    # except Exception as e:
    #     return Response({"error": str(e)}, status=500)


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
