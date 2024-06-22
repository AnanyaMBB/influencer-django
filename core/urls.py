from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/business', views.businessRegister, name='businessRegister'),
    path('api/register/influencer', views.influencerRegister, name='influencerRegister'),
    path('api/influencer/instagram', views.influencerInstagramInformationAdd, name='influencerInstagramInformationAdd')
]