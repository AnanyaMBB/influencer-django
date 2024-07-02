from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/business', views.businessRegister, name='businessRegister'),
    path('api/register/influencer', views.influencerRegister, name='influencerRegister'),
    path('api/influencer/instagram', views.influencerInstagramInformationAdd, name='influencerInstagramInformationAdd'),
    path('api/influencer/instagram/get', views.influencerInstagramInformationGet, name='influencerInstagramInformationGet'),
    path('api/instagram/ugc/add', views.UGCServiceAdd, name='UGCServiceAdd'),
    path('api/instagram/ugc/get', views.UGCServiceGet, name='UGCServiceGet'),   
    path('api/instagram/feed/add', views.FeedPostServiceAdd, name='FeedPostServiceAdd'),
    path('api/instagram/feed/get', views.FeedPostServiceGet, name='FeedPostServiceGet'),
    path('api/instagram/story/add', views.StoryPostServiceAdd, name='StoryPostServiceAdd'),
    path('api/instagram/story/get', views.StoryPostServiceGet, name='StoryPostServiceGet'),
    path('api/instagram/reel/add', views.ReelPostServiceAdd, name='ReelPostServiceAdd'),
    path('api/instagram/reel/get', views.ReelPostServiceGet, name='ReelPostServiceGet'),
    path('api/instagram/other/add', views.OtherServiceAdd, name='OtherServiceAdd'),
    path('api/instagram/other/get', views.OtherServiceGet, name='OtherServiceGet'),
]