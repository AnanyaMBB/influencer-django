from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django_countries.fields import CountryField
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete



class BusinessAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_industry = models.CharField(max_length=100, null=True, blank=True)
    company_website = models.CharField(max_length=100, null=True, blank=True)
    company_size = models.IntegerField(null=True, blank=True)
    company_email = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.CharField(max_length=100, null=True, blank=True)
    company_phone = models.CharField(max_length=100, null=True, blank=True)
    company_city = models.CharField(max_length=100, null=True, blank=True)
    company_state = models.CharField(max_length=100, null=True, blank=True)
    company_zip = models.CharField(max_length=100, null=True, blank=True)
    company_country = models.CharField(max_length=100, null=True, blank=True)


class InfluencerAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class InfluencerInstagramInformation(models.Model):
    influencer = models.ForeignKey(InfluencerAccount, on_delete=models.CASCADE)
    instagram_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    long_access_token = models.CharField(max_length=300, null=True, blank=True)


class InstagramBase(models.Model):
    influencer_instagram_information = models.ForeignKey(
        InfluencerInstagramInformation, on_delete=models.CASCADE
    )
    date = models.DateTimeField(default=datetime.now, null=True, blank=True)


class InstagramInitialInformation(InstagramBase):
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    profile_picture_url = models.CharField(max_length=1000, null=True, blank=True)
    biography = models.CharField(max_length=100, null=True, blank=True)
    followers_count = models.IntegerField(null=True, blank=True)
    follows_count = models.IntegerField(null=True, blank=True)
    media_count = models.IntegerField(null=True, blank=True)
    website = models.CharField(max_length=1000, null=True, blank=True)


class InstagramDetails(InstagramBase):
    likes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    saves = models.IntegerField(null=True, blank=True)
    shares = models.IntegerField(null=True, blank=True)
    replies = models.IntegerField(null=True, blank=True)
    profile_links_taps = models.IntegerField(null=True, blank=True)
    website_clicks = models.IntegerField(null=True, blank=True)
    profile_views = models.IntegerField(null=True, blank=True)
    impressions = models.IntegerField(null=True, blank=True)
    reach = models.IntegerField(null=True, blank=True)
    total_interactions = models.IntegerField(null=True, blank=True)
    accounts_engaged = models.IntegerField(null=True, blank=True)


class InstagramGenderDemographics(InstagramBase):
    type_identifier = models.IntegerField(null=True, blank=True)

    this_week_male = models.IntegerField(null=True, blank=True)
    this_week_female = models.IntegerField(null=True, blank=True)
    this_week_unknown = models.IntegerField(null=True, blank=True)

    this_month_male = models.IntegerField(null=True, blank=True)
    this_month_female = models.IntegerField(null=True, blank=True)
    this_month_unknown = models.IntegerField(null=True, blank=True)

    prev_month_male = models.IntegerField(null=True, blank=True)
    prev_month_female = models.IntegerField(null=True, blank=True)
    prev_month_unknown = models.IntegerField(null=True, blank=True)

    last_14_days_male = models.IntegerField(null=True, blank=True)
    last_14_days_female = models.IntegerField(null=True, blank=True)
    last_14_days_unknown = models.IntegerField(null=True, blank=True)

    last_30_days_male = models.IntegerField(null=True, blank=True)
    last_30_days_female = models.IntegerField(null=True, blank=True)
    last_30_days_unknown = models.IntegerField(null=True, blank=True)

    last_90_days_male = models.IntegerField(null=True, blank=True)
    last_90_days_female = models.IntegerField(null=True, blank=True)
    last_90_days_unknown = models.IntegerField(null=True, blank=True)


class InstagramAgeDemographics(InstagramBase):
    type_identifier = models.IntegerField(null=True, blank=True)

    this_week_13_17 = models.IntegerField(null=True, blank=True)
    this_week_18_24 = models.IntegerField(null=True, blank=True)
    this_week_25_34 = models.IntegerField(null=True, blank=True)
    this_week_35_44 = models.IntegerField(null=True, blank=True)
    this_week_45_54 = models.IntegerField(null=True, blank=True)
    this_week_55_64 = models.IntegerField(null=True, blank=True)
    this_week_65 = models.IntegerField(null=True, blank=True)

    this_month_13_17 = models.IntegerField(null=True, blank=True)
    this_month_18_24 = models.IntegerField(null=True, blank=True)
    this_month_25_34 = models.IntegerField(null=True, blank=True)
    this_month_35_44 = models.IntegerField(null=True, blank=True)
    this_month_45_54 = models.IntegerField(null=True, blank=True)
    this_month_55_64 = models.IntegerField(null=True, blank=True)
    this_month_65 = models.IntegerField(null=True, blank=True)

    prev_month_13_17 = models.IntegerField(null=True, blank=True)
    prev_month_18_24 = models.IntegerField(null=True, blank=True)
    prev_month_25_34 = models.IntegerField(null=True, blank=True)
    prev_month_35_44 = models.IntegerField(null=True, blank=True)
    prev_month_45_54 = models.IntegerField(null=True, blank=True)
    prev_month_55_64 = models.IntegerField(null=True, blank=True)
    prev_month_65 = models.IntegerField(null=True, blank=True)

    last_14_days_13_17 = models.IntegerField(null=True, blank=True)
    last_14_days_18_24 = models.IntegerField(null=True, blank=True)
    last_14_days_25_34 = models.IntegerField(null=True, blank=True)
    last_14_days_35_44 = models.IntegerField(null=True, blank=True)
    last_14_days_45_54 = models.IntegerField(null=True, blank=True)
    last_14_days_55_64 = models.IntegerField(null=True, blank=True)
    last_14_days_65 = models.IntegerField(null=True, blank=True)

    last_30_days_13_17 = models.IntegerField(null=True, blank=True)
    last_30_days_18_24 = models.IntegerField(null=True, blank=True)
    last_30_days_25_34 = models.IntegerField(null=True, blank=True)
    last_30_days_35_44 = models.IntegerField(null=True, blank=True)
    last_30_days_45_54 = models.IntegerField(null=True, blank=True)
    last_30_days_55_64 = models.IntegerField(null=True, blank=True)
    last_30_days_65 = models.IntegerField(null=True, blank=True)

    last_90_days_13_17 = models.IntegerField(null=True, blank=True)
    last_90_days_18_24 = models.IntegerField(null=True, blank=True)
    last_90_days_25_34 = models.IntegerField(null=True, blank=True)
    last_90_days_35_44 = models.IntegerField(null=True, blank=True)
    last_90_days_45_54 = models.IntegerField(null=True, blank=True)
    last_90_days_55_64 = models.IntegerField(null=True, blank=True)
    last_90_days_65 = models.IntegerField(null=True, blank=True)


class InstagramCityDemographics(InstagramBase):
    count = models.IntegerField(null=True, blank=True)
    type_identifier = models.IntegerField(null=True, blank=True)

    this_week_city = models.CharField(max_length=100, null=True, blank=True)
    this_week_follower_count = models.IntegerField(null=True, blank=True)

    this_month_city = models.CharField(max_length=100, null=True, blank=True)
    this_month_follower_count = models.IntegerField(null=True, blank=True)

    prev_month_city = models.CharField(max_length=100, null=True, blank=True)
    prev_month_follower_count = models.IntegerField(null=True, blank=True)

    last_14_days_city = models.CharField(max_length=100, null=True, blank=True)
    last_14_days_follower_count = models.IntegerField(null=True, blank=True)

    last_30_days_city = models.CharField(max_length=100, null=True, blank=True)
    last_30_days_follower_count = models.IntegerField(null=True, blank=True)

    last_90_days_city = models.CharField(max_length=100, null=True, blank=True)
    last_90_days_follower_count = models.IntegerField(null=True, blank=True)


class InstagramCountryDemographics(InstagramBase):
    count = models.IntegerField(null=True, blank=True)
    type_identifier = models.IntegerField(null=True, blank=True)

    this_week_country = CountryField(max_length=100, null=True, blank=True)
    this_week_follower_count = models.IntegerField(null=True, blank=True)

    this_month_country = CountryField(max_length=100, null=True, blank=True)
    this_month_follower_count = models.IntegerField(null=True, blank=True)

    prev_month_country = CountryField(max_length=100, null=True, blank=True)
    prev_month_follower_count = models.IntegerField(null=True, blank=True)

    last_14_days_country = CountryField(max_length=100, null=True, blank=True)
    last_14_days_follower_count = models.IntegerField(null=True, blank=True)

    last_30_days_country = CountryField(max_length=100, null=True, blank=True)
    last_30_days_follower_count = models.IntegerField(null=True, blank=True)

    last_90_days_country = CountryField(max_length=100, null=True, blank=True)
    last_90_days_follower_count = models.IntegerField(null=True, blank=True)


class InstagramMediaData(InstagramBase):
    caption = models.CharField(max_length=1000, null=True, blank=True)
    media_id = models.CharField(max_length=100, null=True, blank=True)
    media_url = models.CharField(max_length=1000, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    comments_count = models.IntegerField(null=True, blank=True)
    saved = models.IntegerField(null=True, blank=True)
    shares = models.IntegerField(null=True, blank=True)
    is_comment_enabled = models.CharField(max_length=10, null=True, blank=True)
    is_share_to_feed = models.CharField(max_length=10, null=True, blank=True)
    media_product_type = models.CharField(max_length=100, null=True, blank=True)
    media_type = models.CharField(max_length=100, null=True, blank=True)
    thumbnail_url = models.CharField(max_length=1000, null=True, blank=True)
    impressions = models.IntegerField(null=True, blank=True)
    reach = models.IntegerField(null=True, blank=True)
    video_views = models.IntegerField(null=True, blank=True)

    ig_reels_avg_watch_time = models.IntegerField(null=True, blank=True)
    ig_reels_video_view_total_time = models.IntegerField(null=True, blank=True)
    plays = models.IntegerField(null=True, blank=True)
    total_interactions = models.IntegerField(null=True, blank=True)
    profile_activity = models.IntegerField(null=True, blank=True)
    profile_visits = models.IntegerField(null=True, blank=True)

    transcribed = models.BooleanField(default=False)


# @receiver(post_save, sender=InstagramMediaData)
# def update_media_data(sender, instance, created, **kwargs):
#     mq = marqo.Client(url="http://localhost:8882")
#     if created:
#         mq.index("instagram_media_data").add_documents(
#             [
#                 {
#                     "id": instance.id,
#                     "media_id": instance.media_id,
#                     "media_type": instance.media_type,
#                     "media_product_type": instance.media_product_type,
#                     "caption": instance.caption,
#                     "media": instance.media_url,
#                 }
#             ]
#         )

#     else:
#         mq.index("instagram_media_data").update_documents(
#             [
#                 {
#                     "id": instance.id,
#                     "media_id": instance.media_id,
#                     "media_type": instance.media_type,
#                     "media_product_type": instance.media_product_type,
#                     "caption": instance.caption,
#                     "media": instance.media_url,
#                 }
#             ]
#         )


# def delete_video_index(sender, instance, **kwargs):
#     mq = marqo.Client(url="http://localhost:8882")
#     mq.index("instagram_media_data").delete_documents([instance.id])


class InstagramMediaComment(InstagramBase):
    media_id = models.ForeignKey(InstagramMediaData, on_delete=models.CASCADE)
    comment_id = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.now, null=True, blank=True)
    text = models.CharField(max_length=1000, null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    user = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    # comment_username = models.CharField(max_length=100, null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    hidden = models.CharField(max_length=10, null=True, blank=True)


class BaseService(models.Model):
    instagram_information = models.ForeignKey(
        InfluencerInstagramInformation, on_delete=models.CASCADE
    )
    service_name = models.CharField(max_length=100, null=True, blank=True)
    service_description = models.CharField(max_length=100, null=True, blank=True)
    post_type = models.CharField(max_length=100, null=True, blank=True)
    post_length = models.IntegerField(null=True, blank=True)
    post_length_applicable = models.BooleanField(default=False)


class UGCService(BaseService):
    post_price = models.FloatField(null=True, blank=True)


class FeedPostService(BaseService):
    post_price_per_hour = models.FloatField(null=True, blank=True)


class StoryPostService(BaseService):
    post_price_per_hour = models.FloatField(null=True, blank=True)


class ReelPostService(BaseService):
    post_price_per_hour = models.FloatField(null=True, blank=True)


class OtherService(BaseService):
    custom_fields = JSONField(default=dict, blank=True, null=True)
    price = models.FloatField(null=True, blank=True)

class Service(models.Model):
    influencer_instagram_information = models.ForeignKey(InfluencerInstagramInformation, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100, null=True, blank=True)
    service_type = models.CharField(max_length=100, null=True, blank=True)
    post_type = models.CharField(max_length=100, null=True, blank=True)
    post_length = models.IntegerField(null=True, blank=True)
    content_provider = models.CharField(max_length=100, null=True, blank=True)

class ServicePricing(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="pricings")
    pricing_type = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
                                              



# {
# "username": "ananya",
# "password": "ananya",
# "email": "ananyabesufekad@gmail.com",
# "BusinessAccount": {
# "first_name":"fdjdjkfdjk",
# "last_name": "djkdfjk",
# "company_name":"jdfkjfkd"
# }
# }


class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    contract_name = models.CharField(max_length=100, null=True, blank=True)
    business = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    influencer = models.ForeignKey(InfluencerAccount, on_delete=models.CASCADE)
    influencerInstagramInformation = models.ForeignKey(InfluencerInstagramInformation, on_delete=models.CASCADE, null=True, blank=True)
    contract_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    document_id = models.CharField(max_length=500, null=True, blank=True)

class ContractVersion(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    contract_version = models.IntegerField()
    contract_text = models.TextField(null=True, blank=True)
    contract_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    contract_visible = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_influencer = models.BooleanField(default=False)
    # file_uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='file_uploader')
    file_uploader = models.CharField(max_length=100, null=True, blank=True)
    file_upload_date = models.DateTimeField(default=datetime.now, null=True, blank=True)

    class Meta: 
        unique_together = ('contract', 'contract_version')
    
    def save(self, *args, **kwargs): 
        if self.pk is None: 
            last_version = ContractVersion.objects.filter(contract=self.contract).order_by('contract_version').last()
            if last_version: 
                self.contract_version = last_version.contract_version + 1
            else: 
                self.contract_version = 1
        super().save(*args, **kwargs)

class ContractUserPermissions(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    user_add_date_time = models.DateTimeField(default=datetime.now, null=True, blank=True)
    

class ContractVersionUserPermissions(models.Model):
    contract_version = models.ForeignKey(ContractVersion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)

    
class SignatureRequests(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    contract_version = models.ForeignKey(ContractVersion, on_delete=models.CASCADE)
    request_user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    file = models.ForeignKey('Files', on_delete=models.CASCADE, null=True, blank=True)

    class Meta: 
        unique_together = ('contract', 'contract_version', 'request_user', 'request_date')

class Files(models.Model):
    file = models.FileField(upload_to='contracts/')
    file_name = models.CharField(max_length=100, null=True, blank=True)
    file_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    file_size = models.PositiveBigIntegerField()
    users = models.ManyToManyField(User, related_name='files')

class Requests(models.Model):
    business = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    influencer = models.ForeignKey(InfluencerAccount, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, null=True, blank=True)
    request_date = models.DateTimeField(default=datetime.now, null=True, blank=True)




# from django.db import models
# from datetime import datetime

# # Base model for YouTube data
# class YouTubeBase(models.Model):
#     date = models.DateTimeField(default=datetime.now, null=True, blank=True)

#     class Meta:
#         abstract = True

# # Model to store basic information about a YouTube channel
# class YouTubeChannelInformation(models.Model):
#     influencer = models.ForeignKey(InfluencerAccount, on_delete=models.CASCADE)
#     channel_id = models.CharField(unique=True, max_length=100)
#     title = models.CharField(max_length=255, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     custom_url = models.CharField(max_length=255, null=True, blank=True)
#     published_at = models.DateTimeField(null=True, blank=True)
#     thumbnail_url = models.CharField(max_length=1000, null=True, blank=True)
#     country = models.CharField(max_length=100, null=True, blank=True)
#     view_count = models.IntegerField(null=True, blank=True)
#     subscriber_count = models.IntegerField(null=True, blank=True)
#     video_count = models.IntegerField(null=True, blank=True)
#     hidden_subscriber_count = models.BooleanField(default=False)

# # Model to store detailed analytics data for a YouTube channel
# class YouTubeChannelAnalytics(YouTubeBase):
#     channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
#     views = models.IntegerField(null=True, blank=True)
#     estimated_minutes_watched = models.IntegerField(null=True, blank=True)
#     average_view_duration = models.IntegerField(null=True, blank=True)
#     total_interactions = models.IntegerField(null=True, blank=True)
#     likes = models.IntegerField(null=True, blank=True)
#     dislikes = models.IntegerField(null=True, blank=True)
#     comments = models.IntegerField(null=True, blank=True)
#     shares = models.IntegerField(null=True, blank=True)

# # Model to store video-specific information
# class YouTubeVideoInformation(models.Model):
#     channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
#     video_id = models.CharField(unique=True, max_length=100)
#     title = models.CharField(max_length=255, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     published_at = models.DateTimeField(null=True, blank=True)
#     thumbnail_url = models.CharField(max_length=1000, null=True, blank=True)
#     duration = models.DurationField(null=True, blank=True)

# # Model to store analytics data for a specific video
# class YouTubeVideoAnalytics(YouTubeBase):
#     video_information = models.ForeignKey(YouTubeVideoInformation, on_delete=models.CASCADE)
#     views = models.IntegerField(null=True, blank=True)
#     estimated_minutes_watched = models.IntegerField(null=True, blank=True)
#     average_view_duration = models.IntegerField(null=True, blank=True)
#     likes = models.IntegerField(null=True, blank=True)
#     dislikes = models.IntegerField(null=True, blank=True)
#     comments = models.IntegerField(null=True, blank=True)
#     shares = models.IntegerField(null=True, blank=True)
#     impressions = models.IntegerField(null=True, blank=True)
#     reach = models.IntegerField(null=True, blank=True)

# # Model to store demographic data related to gender
# class YouTubeGenderDemographics(YouTubeBase):
#     channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
#     male_percentage = models.FloatField(null=True, blank=True)
#     female_percentage = models.FloatField(null=True, blank=True)
#     unknown_percentage = models.FloatField(null=True, blank=True)

# # Model to store demographic data related to age groups
# class YouTubeAgeDemographics(YouTubeBase):
#     channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
#     age_group_13_17 = models.FloatField(null=True, blank=True)
#     age_group_18_24 = models.FloatField(null=True, blank=True)
#     age_group_25_34 = models.FloatField(null=True, blank=True)
#     age_group_35_44 = models.FloatField(null=True, blank=True)
#     age_group_45_54 = models.FloatField(null=True, blank=True)
#     age_group_55_64 = models.FloatField(null=True, blank=True)
#     age_group_65_plus = models.FloatField(null=True, blank=True)

# # Model to store geographic demographic data
# class YouTubeGeographicDemographics(YouTubeBase):
#     channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
#     country = models.CharField(max_length=100, null=True, blank=True)
#     percentage = models.FloatField(null=True, blank=True)



from django.db import models
from datetime import datetime

# Base model for YouTube data
class YouTubeBase(models.Model):
    date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    influencer = models.ForeignKey(InfluencerAccount, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

# Model to store basic information about a YouTube channel
class YouTubeChannelInformation(YouTubeBase):
    channel_id = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    custom_url = models.CharField(max_length=255, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    thumbnail_url = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    view_count = models.IntegerField(null=True, blank=True)
    subscriber_count = models.IntegerField(null=True, blank=True)
    video_count = models.IntegerField(null=True, blank=True)
    hidden_subscriber_count = models.BooleanField(default=False)
    access_token = models.CharField(max_length=300, null=True, blank=True)
    refresh_token = models.CharField(max_length=300, null=True, blank=True)  # Add this field
    token_expiry = models.DateTimeField(null=True, blank=True)  # Add this field to track expiry time


# Model to store detailed analytics data for a YouTube channel
class YouTubeChannelAnalytics(YouTubeBase):
    channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
    views = models.IntegerField(null=True, blank=True)
    estimated_minutes_watched = models.IntegerField(null=True, blank=True)
    average_view_duration = models.IntegerField(null=True, blank=True)
    total_interactions = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    dislikes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    shares = models.IntegerField(null=True, blank=True)

# Model to store video-specific information
class YouTubeVideoInformation(models.Model):
    channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
    video_id = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    thumbnail_url = models.CharField(max_length=1000, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

# Model to store analytics data for a specific video
class YouTubeVideoAnalytics(YouTubeBase):
    video_information = models.ForeignKey(YouTubeVideoInformation, on_delete=models.CASCADE)
    views = models.IntegerField(null=True, blank=True)
    estimated_minutes_watched = models.IntegerField(null=True, blank=True)
    average_view_duration = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    dislikes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    shares = models.IntegerField(null=True, blank=True)
    impressions = models.IntegerField(null=True, blank=True)
    reach = models.IntegerField(null=True, blank=True)

# Model to store demographic data related to gender
class YouTubeGenderDemographics(YouTubeBase):
    channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
    male_percentage = models.FloatField(null=True, blank=True)
    female_percentage = models.FloatField(null=True, blank=True)
    unknown_percentage = models.FloatField(null=True, blank=True)

# Model to store demographic data related to age groups
class YouTubeAgeDemographics(YouTubeBase):
    channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
    age_group_13_17 = models.FloatField(null=True, blank=True)
    age_group_18_24 = models.FloatField(null=True, blank=True)
    age_group_25_34 = models.FloatField(null=True, blank=True)
    age_group_35_44 = models.FloatField(null=True, blank=True)
    age_group_45_54 = models.FloatField(null=True, blank=True)
    age_group_55_64 = models.FloatField(null=True, blank=True)
    age_group_65_plus = models.FloatField(null=True, blank=True)

# Model to store geographic demographic data
class YouTubeGeographicDemographics(YouTubeBase):
    channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)


class YoutubeService(models.Model):
    channel_information = models.ForeignKey(YouTubeChannelInformation, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100, null=True, blank=True)
    service_type = models.CharField(max_length=100, null=True, blank=True)
    post_type = models.CharField(max_length=100, null=True, blank=True)
    post_length = models.IntegerField(null=True, blank=True)
    content_provider = models.CharField(max_length=100, null=True, blank=True)

class YoutubeServicePricing(models.Model):
    service = models.ForeignKey(YoutubeService, on_delete=models.CASCADE, related_name="youtube_pricings")
    pricing_type = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

class YoutubeRequests(models.Model):
    business = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    influencer = models.ForeignKey(InfluencerAccount, on_delete=models.CASCADE)
    service = models.ForeignKey(YoutubeService, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, null=True, blank=True)
    request_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
