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
    path("api/contract/get/account", views.getContractByAccount, name="getContractByAccount"),
    path("api/contract/version/create", views.createNewVersion, name="createNewVersion"),
    path("api/contract/version/get", views.getContractVersions, name="getContractVersions"),
    path("api/contract/version/get/account", views.getContractVersionsByAccount, name="getContractVersionsByAccount"),
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

    path("api/signnow/webhook/", views.signnow_webhook, name="signnow_webhook"),
    path("api/signnow/webhook", views.signnow_webhook, name="signnow_webhook"),

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

    path("api/influencer/youtube/get", views.getYoutubeChannelInformation, name="getYoutubeChannelInformation"),
    path("api/youtube-analytics", views.youtubeAnalytics, name="youtubeAnalytics"),
    path("api/youtube-analytics/get", views.getYoutubeAnalytics, name="getYoutubeAnalytics"),

    path("api/youtube/service/add", views.addYoutubeService, name="addYoutubeService"),
    path("api/youtube/service/get", views.getYoutubeService, name="getYoutubeService"),

    path("api/youtube/filter", views.YoutubeFilterView, name="YoutubeFilterView"),
    path("api/youtube/requests/get", views.getYoutubeRequests, name="getYoutubeRequests"),
    path("api/youtube/requests/send", views.sendYoutubeRequests, name="sendYoutubeRequests"),
    path("api/youtube/requests/state/update", views.updateYoutubeRequestState, name="updateYoutubeRequestState"),

    # path("api/tiktok/account/add", views.addTikTokAccount, name="addTikTokAccount"),
    # path("api/tiktok/account/get", views.getTikTokAccountData, name="getTikTokAccountData"),
    # path("api/tiktok/information/add", views.addTikTokInformation, name="addTiktokInformation"),
    # path("api/tiktok/information/get", views.getTikTokInformation, name="getTiktokInformation"),

    path("api/phyllo/user/get_or_create", views.getCreatePhylloUser, name="getCreatePhylloUser"),
    path("api/phyllo/account/save", views.savePhylloAccount, name="savePhylloAccount"),
    path("api/phyllo/content_data", views.getPhylloContentData, name="getPhylloContentData"),
    path("api/phyllo/content_data/daily", views.getPhylloContentDataDaily, name="getPhylloContentDataDaily"),
    path("api/phyllo/audience_demographics", views.getPhylloAudienceDemographicsData, name="getPhylloAudienceDemographicsData"),
    path("api/phyllo/account/filter", views.filterInfluencerProfiles, name="filterInfluencerProfiles"),
    path("api/phyllo/added_accounts/get", views.getPhylloAddedAccounts, name="getPhylloAddedAccounts"),
    path("api/influencer/service/add", views.addInfluencerService, name="addInfluencerService"),
    path("api/influencer/service/get", views.getInfluencerService, name="getInfluencerService"),
    path("api/campaign/add", views.addCampaign, name="addCampaign"),
    path("api/campaign/get", views.getCampaigns, name="getCampaigns"),
    path("api/campaign_influencer/get", views.getCampaingsForInfluencers, name="getCampaingsForInfluencers"),
    path("api/campaign/influencer/add", views.addInfluencerToCampaign, name="addInfluencerToCampaign"),
    path("api/campaign/influencer/update", views.updateInfluencerCampaignAddStatus, name="updateInfluencerCampaignAddStatus"),
    path("api/campaign/influencer/accept", views.acceptInfluencerCampaign, name="acceptInfluencerCampaign"),
    path("api/campaign/influencer/decline", views.declineInfluencerCampaign, name="declineInfluencerCampaign"),
    path("api/campaign/influencer/get", views.getInfluencersInCampaign, name="getInfluencersInCampaign"),
    path("api/campaign/file/upload", views.uploadCampaignFile, name="uploadCampaignFile"),
    path("api/campaign/file/get/all", views.getCampaignFiles, name="getCampaignFiles"),
    path("api/campaign/post/scheduler", views.schedulePost, name="schedulePost"),
    path("api/campaign/details/get", views.getCampaignDetails, name="getCampaignDetails"),
    path("api/campaign/scheduled/details", views.getCampaignFileScheduledPost, name="getCampaignFileScheduledPost"),
    path("api/campaign/scheduled/accept", views.acceptScheduleRequest, name="acceptScheduledrequest"),
    path("api/campaign/scheduled/remove", views.removeScheduled, name="removeScheduled"),
    path("api/campaign/scheduled/paid", views.markPaymentPaid, name="markPaymentPaid"),
    path("api/campaign/published/success/webhook", views.publishedSuccessWebhook, name="publishedSuccessWebhook"),
    path("api/campaign/published/content_data", views.getPhylloPostedContentData, name="getPhylloPostedContentData"),
    path("api/campaign/scheduled/get", views.getScheduledPosts, name="getScheduledPosts"),
]
