from django.db import models
from django.contrib.auth.models import User 

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
    influencer = models.OneToOneField(InfluencerAccount, on_delete=models.CASCADE)
    instagram_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    profile_picture_url = models.CharField(max_length=255, null=True, blank=True)
    biography = models.CharField(max_length=100, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    following = models.IntegerField(null=True, blank=True)
    posts = models.IntegerField(null=True, blank=True)
    long_access_token = models.CharField(max_length=300, null=True, blank=True)

    # class Meta: 
    #     indexes = [
    #         models.Index(fields=['username']),
    #         models.Index(fields=['instagram_id'])
    #     ]
    


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