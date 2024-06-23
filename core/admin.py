from django.contrib import admin
from .models import BusinessAccount, InfluencerAccount, InfluencerInstagramInformation, BaseService, UGCService, FeedPostService, StoryPostService, ReelPostService, OtherService
# Register your models here.
admin.site.register(BusinessAccount)
admin.site.register(InfluencerAccount)
admin.site.register(InfluencerInstagramInformation)
admin.site.register(BaseService)
admin.site.register(UGCService)
admin.site.register(FeedPostService)
admin.site.register(StoryPostService)
admin.site.register(ReelPostService)
admin.site.register(OtherService)