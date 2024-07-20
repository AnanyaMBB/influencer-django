from django.shortcuts import render, get_object_or_404, Http404
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
    ServicePricing
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import InfluencerFilter
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django.db.models import Max
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
    user = User.objects.get(username=request.user)
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


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
def InstagramFilterView(request):
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
    contractVersion = ContractVersion.objects.get(contract=contract, contract_version=request.GET.get("version_id"))
    print("Contract Version: ", contractVersion)
    signedRequests = SignatureRequests.objects.get(contract=contract, contract_version=contractVersion, state="accepted")
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
    contract_version = ContractVersion.objects.get(contract=contract, contract_version=request.GET.get("version_id"))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def downloadFile(request):
    file_instance = get_object_or_404(Files, id=request.GET.get("file_id"))
    file_path = file_instance.file.path

    try:
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=file_instance.file_name or file_instance.file.name)
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
    signatureRequests = SignatureRequests.objects.filter(contract=contract, contract_version=contract_version).latest("request_date")
    
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
    influencerInstagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=request.GET.get("instagram_id"))
    services = Service.objects.filter(influencer_instagram_information=influencerInstagramInformation)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

