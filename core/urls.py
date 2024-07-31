from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accountType", views.accountType, name="accountType"),
    path("api/register/business", views.businessRegister, name="businessRegister"),
    path(
        "api/register/influencer", views.influencerRegister, name="influencerRegister"
    ),
    path(
        "api/influencer/instagram",
        views.influencerInstagramInformationAdd,
        name="influencerInstagramInformationAdd",
    ),
    path(
        "api/influencer/instagram/get",
        views.influencerInstagramInformationGet,
        name="influencerInstagramInformationGet",
    ),
    path("api/instagram/ugc/add", views.UGCServiceAdd, name="UGCServiceAdd"),
    path("api/instagram/ugc/get", views.UGCServiceGet, name="UGCServiceGet"),
    path("api/instagram/feed/add", views.FeedPostServiceAdd, name="FeedPostServiceAdd"),
    path("api/instagram/feed/get", views.FeedPostServiceGet, name="FeedPostServiceGet"),
    path(
        "api/instagram/story/add", views.StoryPostServiceAdd, name="StoryPostServiceAdd"
    ),
    path(
        "api/instagram/story/get", views.StoryPostServiceGet, name="StoryPostServiceGet"
    ),
    path("api/instagram/reel/add", views.ReelPostServiceAdd, name="ReelPostServiceAdd"),
    path("api/instagram/reel/get", views.ReelPostServiceGet, name="ReelPostServiceGet"),
    path("api/instagram/other/add", views.OtherServiceAdd, name="OtherServiceAdd"),
    path("api/instagram/other/get", views.OtherServiceGet, name="OtherServiceGet"),
    path(
        "api/instagram/data/details",
        views.InstagramDetailsGet,
        name="InstagramDetailsGet",
    ),
    path(
        "api/instagram/data/media",
        views.InstagramMediaDataGet,
        name="InstagramMediaDataGet",
    ),
    path(
        "api/instagram/data/demographics/age",
        views.InstagramAgeDemographicsGet,
        name="InstagramAgeDemographicsGet",
    ),
    path(
        "api/instagram/data/demographics/gender",
        views.InstagramGenderDemographicsGet,
        name="InstagramGenderDemographicsGet",
    ),
    path(
        "api/instagram/data/demographics/city",
        views.InstagramCityDemographicsGet,
        name="InstagramCityDemographicsGet",
    ),
    path(
        "api/instagram/data/demographics/country",
        views.InstagramCountryDemographicsGet,
        name="InstagramCountryDemographicsGet",
    ),

    path("api/instagram/filter", views.InstagramFilterView, name="InstagramFilterView"), 

    # Contract
    path("api/contract/create", views.createContract, name="createContract"),
    path("api/contract/get", views.getContract, name="getContract"),    
    path("api/contract/get/all", views.getContractAll, name="getContractAll"),
    path("api/contract/version/create", views.createNewVersion, name="createNewVersion"),
    path("api/contract/version/get", views.getContractVersions, name="getContractVersions"),
    path("api/contract/version/text/get", views.getContractVersionText, name="getContractVersionText"),
    path("api/contract/version/update", views.updateContractVersionText, name="updateContractVersion"),
    path("api/contract/signature/request", views.addSignatureRequest, name="addSignatureRequest"),
    path("api/contract/signature/get", views.getSignatureState, name="getSignatureState"),
    path("api/contract/signature/accept", views.acceptSignature, name="acceptSignature"),
    path("api/contract/signature/decline", views.declineSignature, name="declineSignature"),

    path("api/contract/signature/document/upload", views.uploadDocumentSignNow, name="uploadDocumentSignNow"),
    path("api/contract/signature/invite", views.inviteSignNow, name="inviteSignNow"),
    path("api/contract/signed", views.getSignedContracts, name="getSignedContracts"),
    path("api/contract/signed/get", views.getSignedContract, name="getSignedContract"),

    path("api/files", views.getUserFiles, name="getUserFiles"),

    path("api/element/details", views.getElementDetails, name="getElementDetails"),

    path("api/file/download", views.downloadFile, name="downloadFile"),
    path("api/file/upload", views.uploadFile, name="uploadFile"),

    path("api/campaign/file/update", views.updateCampaignFile, name="updateCampaignFile"),

    path("api/instagram/service/add", views.addInstagramService, name="addInstagramService"),
    path("api/instagram/service/get", views.getInstagramService, name="getInstagramService"),

    path("api/requests/get", views.getRequests, name="getRequests"),
    path("api/requests/send", views.sendRequests, name="sendRequests"),
    path("api/requests/state/update", views.updateRequestState, name="updateRequestState"),

    path("api/research/search", views.searchReels, name="searchReels"),
]
