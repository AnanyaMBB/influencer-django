from django.core.management.base import BaseCommand
from django.utils import timezone
import core.models
import requests
from datetime import datetime
from django.utils.dateparse import parse_datetime
import base64

class Command(BaseCommand):
    help = "Updates the database with the latest information from the Phyllo API."

    def handle(self, *args, **options):
        self.stdout.write('Updating Phyllo information...')
        self.update()

    def update(self):
        phylloAccounts = core.models.PhylloAccount.objects.all() 
        print(phylloAccounts)
        for phylloAccount in phylloAccounts: 
            phylloAddedAccounts = core.models.PhylloAddedAccounts.objects.filter(phyllo_account=phylloAccount)
            print(phylloAddedAccounts)
            for phylloAddedAccount in phylloAddedAccounts: 
                try: 
                    profileData = self.getPhylloProfile(phylloAddedAccount.phyllo_accountid)
                    engagementData = self.getPhylloEngagement(phylloAddedAccount.phyllo_accountid)
                    audienceDemographicsData = self.getAudienceDemographics(phylloAddedAccount.phyllo_accountid)
                    
                    gender_totals = {'MALE': 0, 'FEMALE': 0, 'OTHER': 0}  # Include all genders
                    age_totals = {
                        '13-17': 0,
                        '18-24': 0,
                        '25-32': 0,
                        '33-39': 0,
                        '40-49': 0,
                        '50-59': 0,
                        '60+': 0
                    } 

                    print("audienceDemographicsData", audienceDemographicsData)

                    if audienceDemographicsData: 
                        for entry in audienceDemographicsData["gender_age_distribution"]:
                            gender = entry['gender']
                            age_range = entry['age_range']
                            value = entry['value']
                            
                            # Accumulate gender totals
                            if gender in gender_totals:
                                gender_totals[gender] += value
                            
                            # Accumulate age totals
                            if age_range in age_totals:
                                age_totals[age_range] += value

                        # Calculate total percentage
                        total_value = sum(gender_totals.values())

                        # Calculate percentages
                        gender_percentages = {k: (v / total_value) * 100 for k, v in gender_totals.items()}
                        age_percentages = {k: (v / total_value) * 100 for k, v in age_totals.items()}

                        audienceDemographics = core.models.PhylloAudienceDemographics(
                            phyllo_account = phylloAddedAccount,
                            phyllo_gender_demographics_male = gender_percentages["MALE"],
                            phyllo_gender_demographics_female = gender_percentages["FEMALE"],
                            phyllo_gender_demographics_other = gender_percentages["OTHER"],
                            phyllo_age_13_17 = age_percentages["13-17"],
                            phyllo_age_18_24 = age_percentages["18-24"],
                            phyllo_age_25_32 = age_percentages["25-32"],
                            phyllo_age_33_39 = age_percentages["33-39"],
                            phyllo_age_40_49 = age_percentages["40-49"],
                            phyllo_age_50_59 = age_percentages["50-59"],
                            phyllo_age_60_plus = age_percentages["60+"]
                        )

                        audienceDemographics.save()

                        for country in audienceDemographicsData["countries"]:
                            phylloAudienceCountryDemographics = core.models.PhylloAudienceCountryDemographics(
                                demographics = audienceDemographics,
                                country_code = country.get("code", None),
                                percentage = country.get("value", None)
                            )

                            phylloAudienceCountryDemographics.save()

                        for city in audienceDemographicsData["countries"]:
                            phylloAudienceCityDemographics = core.models.PhylloAudienceCityDemographics(
                                demographics = audienceDemographics,
                                city = city.get("code", None),
                                percentage = city.get("value", None)
                            )

                            phylloAudienceCountryDemographics.save()

                    for data in profileData["data"]: 
                        phylloAccountProfile = core.models.PhylloAccountProfile(
                            phyllo_account=phylloAddedAccount,
                            phyllo_id = data["id"],
                            phyllo_created_at = parse_datetime(data.get("created_at", None)) if data.get("created_at") else None, 
                            phyllo_updated_at = parse_datetime(data.get("updated_at", None)) if data.get("updated_at") else None,
                            phyllo_user_id = data.get("user", {}).get("id", None),
                            phyllo_user_name = data.get("user", {}).get("name", None),
                            phyllo_accountid = data.get("account", {}).get("id", None),
                            phyllo_account_platform_username = data.get("account", {}).get("platform_username", None),
                            phyllo_work_platform_id = data.get("work_platform", {}).get("id", None),
                            phyllo_work_platform_name = data.get("work_platform", {}).get("name", None),
                            phyllo_work_platform_logo_url = data.get("work_platform", {}).get("logo_url", None),
                            phyllo_platform_username = data.get("platform_username", None),
                            phyllo_full_name = data.get("full_name", None),
                            phyllo_first_name = data.get("first_name", None),
                            phyllo_last_name = data.get("last_name", None),
                            phyllo_nick_name = data.get("nick_name", None),
                            phyllo_url = data.get("url", None),
                            phyllo_introduction = data.get("introduction", None),
                            phyllo_image_url = data.get("image_url", None),
                            phyllo_date_of_birth = parse_datetime(data.get("date_of_birth", None)) if data.get("date_of_birth") else None,
                            phyllo_external_id = data.get("external_id", None),
                            phyllo_platform_account_type = data.get("platform_account_type", None),
                            phyllo_category = data.get("category", None),
                            phyllo_website = data.get("website", None),
                            phyllo_reputation_follower_count = data.get("reputation", {}).get("follower_count", None),
                            phyllo_reputation_following_count = data.get("reputation", {}).get("following_count", None),
                            phyllo_reputation_subscriber_count = data.get("reputation", {}).get("subscriber_count", None),
                            phyllo_reputation_content_count = data.get("reputation", {}).get("content_count", None),
                            phyllo_reputation_content_group_count = data.get("reputation", {}).get("content_group_count", None),
                            phyllo_watch_time_in_hours = data.get("watch_time_in_hours", None),
                            phyllo_emails = data.get("emails", None),
                            phyllo_phone_numbers = data.get("phone_numbers", None),
                            phyllo_addresses = data.get("addresses", None),
                            phyllo_gender = data.get("gender", None), 
                            phyllo_country = data.get("country", None),
                            phyllo_platform_profile_name = data.get("platform_profile_name", None),
                            phyllo_platform_profile_id = data.get("platform_profile_id", None), 
                            phyllo_platform_profile_published_at = parse_datetime(data.get("platform_profile_published_at", None)) if data.get("platform_profile_published_at") else None, 
                            phyllo_is_verified = data.get("is_verified", False),
                            phyllo_is_business = data.get("is_business", False)
                        )

                        phylloAccountProfile.save()

                    for data in engagementData["data"]:
                        phylloContentData = core.models.PhylloContentData(
                            phyllo_account = phylloAddedAccount, 
                            phyllo_contentid = data.get("id", None),
                            phyllo_created_at = parse_datetime(data.get("created_at", None)) if data.get("created_at") else None,
                            phyllo_updated_at = parse_datetime(data.get("updated_at", None)) if data.get("updated_at") else None,
                            phyllo_user_id = data.get("user", {}).get("id", None),
                            phyllo_user_name = data.get("user", {}).get("name", None),
                            phyllo_accountid = data.get("account", {}).get("id", None),
                            phyllo_account_platform_username = data.get("account", {}).get("platform_username", None),
                            phyllo_work_platform_id = data.get("work_platform", {}).get("id", None),
                            phyllo_work_platform_name = data.get("work_platform", {}).get("name", None),
                            phyllo_work_platform_logo_url = data.get("work_platform", {}).get("logo_url", None),
                            phyllo_engagement_like_count = data.get("engagement", {}).get("like_count", None),
                            phyllo_engagement_dislike_count = data.get("engagement", {}).get("dislike_count", None),
                            phyllo_engagement_comment_count = data.get("engagement", {}).get("comment_count", None),
                            phyllo_engagement_impression_organic_count = data.get("engagement", {}).get("impression_organic_count", None),
                            phyllo_engagement_reach_organic_count = data.get("engagement", {}).get("reach_organic_count", None),
                            phyllo_engagement_save_count = data.get("engagement", {}).get("save_count", None),
                            phyllo_engagement_view_count = data.get("engagement", {}).get("view_count", None),  
                            phyllo_engagement_watch_time_in_hours = data.get("engagement", {}).get("watch_time_in_hours", None),
                            phyllo_engagement_share_count = data.get("engagement", {}).get("share_count", None),
                            phyllo_engagement_impression_paid_count = data.get("engagement", {}).get("impression_paid_count", None),
                            phyllo_engagement_reach_paid_count = data.get("engagement", {}).get("reach_paid_count", None),
                            phyllo_external_id = data.get("external_id", None),
                            phyllo_title = data.get("title", None),
                            phyllo_format = data.get("format", None),
                            phyllo_type = data.get("type", None),
                            phyllo_url = data.get("url", None),
                            phyllo_media_url = data.get("media_url", None),
                            phyllo_duration = data.get("duration", None),
                            phyllo_description = data.get("description", None),
                            phyllo_visibility = data.get("visibility", None),
                            phyllo_thumbnail_url = data.get("thumbnail_url", None),
                            phyllo_published_at = data.get("published_at", None),
                            phyllo_platform_profile_id = data.get("platform_profile_id", None),
                            phyllo_platform_profile_name = data.get("platform_profile_name", None),
                            phyllo_sponsored = data.get("sponsored", None),
                            phyllo_collaboration = data.get("collaboration", None)
                        )

                        phylloContentData.save()

                        
                        comments = self.getPhylloComments(account_id=phylloAddedAccount.phyllo_accountid, content_id=data.get("id", None))
                        
                        for comment in comments["data"]: 
                            phylloComments = core.models.PhylloComments(
                                phyllo_content = phylloContentData,
                                phyllo_comment_id = comment.get("id", None),
                                phyllo_created_at = parse_datetime(comment.get("created_at", None)) if comment.get("created_at") else None,
                                phyllo_updated_at = parse_datetime(comment.get("updated_at", None)) if comment.get("updated_at") else None,
                                phyllo_published_at = parse_datetime(comment.get("published_at", None)) if comment.get("published_at") else None,
                                phyllo_user_id = comment.get("user", {}).get("id", None),
                                phyllo_user_name = comment.get("user", {}).get("name", None),
                                phyllo_accountid = comment.get("account", {}).get("id", None),
                                phyllo_platform_username = comment.get("platform_username", None),
                                phyllo_work_platform_id = comment.get("work_platform", {}).get("id", None),
                                pyllo_work_platform_name = comment.get("work_platform", {}).get("name", None),
                                phyllo_logo_url = comment.get("work_platform", {}).get("logo_url", None),
                                phyllo_contentid = comment.get("content", {}).get("id", None),
                                phyllo_content_url = comment.get("content", {}).get("url", None),
                                phyllo_content_published_at = comment.get("content", {}).get("published_at", None),
                                phyllo_external_id = comment.get("external_id", None),
                                phyllo_text = comment.get("text", None),
                                phyllo_commenter_username = comment.get("commenter_username", None),
                                phyllo_commenter_display_name = comment.get("commenter_display_name", None),
                                phyllo_commenter_id = comment.get("commenter_id", None),
                                phyllo_commenter_profile_url = comment.get("commenter_profile_url", None),
                                phyllo_like_count = comment.get("like_count", None),
                                phyllo_reply_count = comment.get("reply_count", None)
                            )

                            phylloComments.save()

                except Exception as e:
                    print("Exception ", e)


    def getPhylloProfile(self, account_id): 
        url = "https://api.staging.insightiq.ai/v1/profiles"
        queryString = {"account_id": account_id}
        # credentials = "70a4fab4-8f91-443a-9330-3349431b5029:e140a14a-788d-4ec0-b0df-d34a8aced66a"
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }
        response = requests.get(url, headers=headers, params=queryString)

        return response.json()
    
    def getPhylloEngagement(self, account_id):
        url = "https://api.staging.insightiq.ai/v1/social/contents"
        queryString = {"account_id": account_id}
        # credentials = "70a4fab4-8f91-443a-9330-3349431b5029:e140a14a-788d-4ec0-b0df-d34a8aced66a"
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            "Accept": "application/json", 
            "Authorization": f"Basic {encoded_credentials}"
        }
        response = requests.get(url, headers=headers, params=queryString)
        return response.json()

    def getPhylloComments(self, account_id, content_id): 
        url = "https://api.staging.insightiq.ai/v1/social/comments"

        querystring = {"account_id":account_id ,"content_id": content_id}
        # credentials = "70a4fab4-8f91-443a-9330-3349431b5029:e140a14a-788d-4ec0-b0df-d34a8aced66a"
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        response = requests.get(url, headers=headers, params=querystring)

        return response.json()
    
    def getAudienceDemographics(self, account_id): 
        url = "https://api.staging.insightiq.ai/v1/audience"
        querystring = {"account_id": account_id}
        # credentials = "70a4fab4-8f91-443a-9330-3349431b5029:e140a14a-788d-4ec0-b0df-d34a8aced66a"
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        response = requests.get(url, headers=headers, params=querystring)

        return response.json()