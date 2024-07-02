from django.db import models
from django.contrib.auth.models import User 
from django.db.models import JSONField
from django_countries.fields import CountryField
from datetime import datetime 

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
    influencer_instagram_information = models.ForeignKey(InfluencerInstagramInformation, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class InstagramInitialInformation(InstagramBase): 
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    profile_picture_url = models.CharField(max_length=1000, null=True, blank=True)
    biography = models.CharField(max_length=100, null=True, blank=True)
    followers_count = models.IntegerField(null=True, blank=True)
    follows_count = models.IntegerField(null=True, blank=True)
    media_count = models.IntegerField(null=True, blank=True)
    website=models.CharField(max_length=1000, null=True, blank=True)

class InstagramDetails(InstagramBase):
    likes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    saved = models.IntegerField(null=True, blank=True)
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
    timestamp = models.DateTimeField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    comment_count = models.IntegerField(null=True, blank=True)
    saved_count = models.IntegerField(null=True, blank=True)
    shares_count = models.IntegerField(null=True, blank=True)
    is_comment_enabled = models.BooleanField(default=False)
    is_share_to_feed = models.BooleanField(default=False)
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

class InstagramMediaComment(InstagramBase):
    media_id = models.ForeignKey(InstagramMediaData, on_delete=models.CASCADE)
    comment_id = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.now, null=True, blank=True)
    text = models.CharField(max_length=1000, null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    comment_user = models.CharField(max_length=100, null=True, blank=True)
    # comment_username = models.CharField(max_length=100, null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    hidden = models.BooleanField(default=False)


class BaseService(models.Model):
    instagram_information = models.ForeignKey(InfluencerInstagramInformation, on_delete=models.CASCADE)
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