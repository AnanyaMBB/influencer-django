from django.db import models
from django.contrib.auth.models import User 
from django.db.models import JSONField

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
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    profile_picture_url = models.CharField(max_length=1000, null=True, blank=True)
    biography = models.CharField(max_length=100, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    following = models.IntegerField(null=True, blank=True)
    posts = models.IntegerField(null=True, blank=True)
    website=models.CharField(max_length=1000, null=True, blank=True)
    long_access_token = models.CharField(max_length=300, null=True, blank=True)


    # class Meta: 
    #     indexes = [
    #         models.Index(fields=['username']),
    #         models.Index(fields=['instagram_id'])
    #     ]

class BaseService(models.Model):
    instagram_information = models.ForeignKey(InfluencerInstagramInformation, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100, null=True, blank=True)
    service_description = models.CharField(max_length=100, null=True, blank=True)
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