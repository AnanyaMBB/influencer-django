from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import (
    InfluencerInstagramInformation,
    InstagramAgeDemographics,
    InstagramGenderDemographics,
    InstagramCityDemographics,
    InstagramCountryDemographics,
    InstagramDetails,
    InstagramMediaData,
    InstagramMediaComment,
)
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Download data from Instagram API and store it in the database'

    def handle(self, *args, **options):
        self.stdout.write("Starting Instagram data update...")
        self.update_info()
        self.prev_info_update()
        self.stdout.write(self.style.SUCCESS("Instagram data update completed successfully!"))

    def update_info(self):
        timeframe = ['this_week', 'this_month', 'prev_month', 'last_14_days', 'last_30_days', 'last_90_days']
        ages = ['_13_17', '_18_24', '_25_34', '_35_44', '_45_54', '_55_64', '_65']
        genders = ['_male', '_female', '_unknown']

        self.update_demographics(timeframe, ages, genders)
        self.update_instagram_details()

    def update_demographics(self, timeframe, ages, genders):
        info_objects = InfluencerInstagramInformation.objects.all()
        
        for info in info_objects:
            self.update_age_demographics(info, timeframe, ages)
            self.update_gender_demographics(info, timeframe, genders)
            self.update_country_demographics(info, timeframe)
            self.update_city_demographics(info, timeframe)

    def update_age_demographics(self, info, timeframe, ages):
        for time in timeframe:
            response = self.get_instagram_data(info, 'follower_demographics', time, 'age')
            if response:
                date = timezone.now()
                for result, age in zip(response['results'], ages):
                    demo_age, _ = InstagramAgeDemographics.objects.get_or_create(
                        instagram_id=info,
                        date=date,
                        type_identifier=0
                    )
                    setattr(demo_age, time + age, result['value'])
                    demo_age.save()
        self.stdout.write("Age demographics updated.")

    def update_gender_demographics(self, info, timeframe, genders):
        for time in timeframe:
            response = self.get_instagram_data(info, 'follower_demographics', time, 'gender')
            if response:
                date = timezone.now()
                for result, gender in zip(response['results'], genders):
                    demo_gender, _ = InstagramGenderDemographics.objects.get_or_create(
                        instagram_id=info,
                        date=date,
                        type_identifier=0
                    )
                    setattr(demo_gender, time + gender, result['value'])
                    demo_gender.save()
        self.stdout.write("Gender demographics updated.")

    def update_country_demographics(self, info, timeframe):
        for time in timeframe:
            response = self.get_instagram_data(info, 'follower_demographics', time, 'country')
            if response:
                date = timezone.now()
                for count, result in enumerate(response['results']):
                    demo_country, _ = InstagramCountryDemgraphics.objects.get_or_create(
                        instagram_id=info,
                        count=count,
                        date=date,
                        type_identifier=0
                    )
                    setattr(demo_country, time + '_country', result['dimension_values'][0])
                    setattr(demo_country, time + '_follower_count', result['value'])
                    demo_country.save()
        self.stdout.write("Country demographics updated.")

    def update_city_demographics(self, info, timeframe):
        for time in timeframe:
            response = self.get_instagram_data(info, 'follower_demographics', time, 'city')
            if response:
                date = timezone.now()
                for count, result in enumerate(response['results']):
                    demo_city, _ = InstagramCityDemographics.objects.get_or_create(
                        instagram_id=info,
                        count=count,
                        date=date,
                        type_identifier=0
                    )
                    setattr(demo_city, time + '_city', result['dimension_values'])
                    setattr(demo_city, time + '_follower_count', result['value'])
                    demo_city.save()
        self.stdout.write("City demographics updated.")

    def update_instagram_details(self):
        items = ['likes', 'comments', 'saves', 'shares', 'replies', 'profile_links_taps',
                 'website_clicks', 'profile_views', 'impressions', 'reach',
                 'total_interactions', 'accounts_engaged']
        
        info_objects = InfluencerInstagramInformation.objects.all()
        
        for info in info_objects:
            date = timezone.now()
            instagram_detail, _ = InstagramDetails.objects.get_or_create(
                instagram_id=info,
                date=date
            )
            
            for item in items:
                response = self.get_instagram_data(info, item, 'day')
                if response:
                    setattr(instagram_detail, item, response['value'])
            
            instagram_detail.save()
        
        self.stdout.write("Instagram details updated.")

    def prev_info_update(self):
        info_objects = InfluencerInstagramInformation.objects.all()
        
        for info in info_objects:
            self.update_media_data(info)

    def update_media_data(self, info):
        response = self.get_instagram_media(info)
        if response:
            for media in response['data']:
                media_data = self.get_media_details(info, media['id'])
                if media_data:
                    self.save_media_data(info, media_data)
                    self.update_media_comments(info, media['id'])

    def save_media_data(self, info, media_data):
        media, _ = InstagramMediaData.objects.get_or_create(
            instagram_id=info,
            media_id=media_data['id'],
            timestamp=media_data['timestamp']
        )
        
        for field in InstagramMediaData._meta.fields:
            if field.name in media_data:
                setattr(media, field.name, media_data[field.name])
        
        media.save()
        self.stdout.write(f"Media data saved for ID: {media_data['id']}")

    def update_media_comments(self, info, media_id):
        comments = self.get_media_comments(info, media_id)
        if comments:
            for comment in comments['data']:
                comment_data = self.get_comment_details(info, comment['id'])
                if comment_data:
                    self.save_comment_data(info, media_id, comment_data)

    def save_comment_data(self, info, media_id, comment_data):
        media = InstagramMediaData.objects.get(instagram_id=info, media_id=media_id)
        comment, _ = InstagramMediaComment.objects.get_or_create(
            instagram_id=info,
            media_id=media,
            comment_id=comment_data['id'],
            timestamp=comment_data['timestamp']
        )
        
        for field in InstagramMediaComment._meta.fields:
            if field.name in comment_data:
                setattr(comment, field.name, comment_data[field.name])
        
        comment.save()
        self.stdout.write(f"Comment data saved for ID: {comment_data['id']}")

    def get_instagram_data(self, info, metric, period, breakdown=None):
        url = f'https://graph.facebook.com/v18.0/{info.i_id}/insights'
        params = {
            'metric': metric,
            'period': period,
            'access_token': info.i_l_access_token
        }
        if breakdown:
            params['breakdown'] = breakdown
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['data'][0]['values'][0]
        else:
            self.stderr.write(f"Error fetching Instagram data: {response.text}")
            return None

    def get_instagram_media(self, info):
        url = f'https://graph.facebook.com/v18.0/{info.i_id}/media'
        params = {'access_token': info.i_l_access_token}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            self.stderr.write(f"Error fetching Instagram media: {response.text}")
            return None

    def get_media_details(self, info, media_id):
        url = f'https://graph.facebook.com/v18.0/{media_id}'
        params = {
            'fields': 'caption,id,timestamp,is_comment_enabled,is_shared_to_feed,like_count,media_product_type,media_type,thumbnail_url,comments_count',
            'access_token': info.i_l_access_token
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            self.stderr.write(f"Error fetching media details: {response.text}")
            return None

    def get_media_comments(self, info, media_id):
        url = f'https://graph.facebook.com/v18.0/{media_id}/comments'
        params = {'access_token': info.i_l_access_token}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            self.stderr.write(f"Error fetching media comments: {response.text}")
            return None

    def get_comment_details(self, info, comment_id):
        url = f'https://graph.facebook.com/v18.0/{comment_id}'
        params = {
            'fields': 'like_count,timestamp,text,parent_id,user',
            'access_token': info.i_l_access_token
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            self.stderr.write(f"Error fetching comment details: {response.text}")
            return None