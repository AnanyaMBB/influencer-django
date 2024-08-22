from django.core.management.base import BaseCommand
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from .models import (
    YouTubeChannelInformation,
    YouTubeChannelAnalytics,
    YouTubeVideoInformation,
    YouTubeVideoAnalytics,
    YouTubeGenderDemographics,
    YouTubeAgeDemographics,
)

def get_or_refresh_credentials(channel_info):
    # Check if the access token is still valid
    if channel_info.token_expiry and channel_info.token_expiry > datetime.now():
        # Token is still valid
        credentials = Credentials(
            token=channel_info.access_token,
            refresh_token=channel_info.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id="119904184627-1ssstt91tkt1lj9lda9e5hb4oi9kiqdo.apps.googleusercontent.com",  # Replace with your client_id
            client_secret="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"  # Replace with your client_secret
        )
    else:
        # Token has expired, refresh it
        credentials = Credentials(
            None,
            refresh_token=channel_info.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id="119904184627-1ssstt91tkt1lj9lda9e5hb4oi9kiqdo.apps.googleusercontent.com",
            client_secret="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"
        )
        credentials.refresh(Request())

        # Update the access token and expiry time in the database
        channel_info.access_token = credentials.token
        channel_info.token_expiry = datetime.now() + timedelta(seconds=credentials.expiry)
        channel_info.save()

    return credentials

class Command(BaseCommand):
    help = 'Update YouTube channel information and analytics daily for all channels in the database'

    def handle(self, *args, **kwargs):
        # Fetch and update all channel information in the database
        channels = YouTubeChannelInformation.objects.all()
        for channel in channels:
            self.stdout.write(f"Updating data for channel: {channel.title}")
            credentials = get_or_refresh_credentials(channel)  # Use the refreshed credentials
            youtube = build('youtube', 'v3', credentials=credentials)
            youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)

            # Fetch and update channel details
            self.update_channel_information(youtube, youtube_analytics, channel)

    def update_channel_information(self, youtube, youtube_analytics, channel_instance):
        try:
            channel_request = youtube.channels().list(part="snippet,statistics,contentDetails", id=channel_instance.channel_id)
            channel_response = channel_request.execute()

            if not channel_response['items']:
                self.stdout.write(self.style.WARNING(f"No data found for channel ID {channel_instance.channel_id}"))
                return

            channel_info = channel_response['items'][0]

            # Update channel details
            channel_instance.title = channel_info['snippet']['title']
            channel_instance.description = channel_info['snippet']['description']
            channel_instance.custom_url = channel_info['snippet'].get('customUrl')
            channel_instance.published_at = channel_info['snippet']['publishedAt']
            channel_instance.thumbnail_url = channel_info['snippet']['thumbnails']['default']['url']
            channel_instance.view_count = channel_info['statistics']['viewCount']
            channel_instance.subscriber_count = channel_info['statistics']['subscriberCount']
            channel_instance.video_count = channel_info['statistics']['videoCount']
            channel_instance.hidden_subscriber_count = channel_info['statistics']['hiddenSubscriberCount']
            channel_instance.save()

            self.update_channel_analytics(youtube_analytics, channel_instance, channel_info)
            self.update_video_information(youtube, youtube_analytics, channel_instance)
            self.update_demographics(youtube_analytics, channel_instance, channel_info)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error updating channel information: {str(e)}"))

    def update_channel_analytics(self, youtube_analytics, channel_instance, channel_info):
        start_date = channel_info['snippet']['publishedAt'].split("T")[0]
        end_date = datetime.now().strftime("%Y-%m-%d")
        analytics_request = youtube_analytics.reports().query(
            ids=f'channel=={channel_instance.channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
            dimensions='day',
            sort='day'
        )
        analytics_response = analytics_request.execute()

        for row in analytics_response.get('rows', []):
            YouTubeChannelAnalytics.objects.update_or_create(
                channel_information=channel_instance,
                date=datetime.strptime(row[0], '%Y-%m-%d'),
                defaults={
                    'views': row[1],
                    'estimated_minutes_watched': row[2],
                    'average_view_duration': row[3],
                    'likes': row[4],
                    'dislikes': row[5],
                    'comments': row[6],
                    'shares': row[7],
                }
            )

    def update_video_information(self, youtube, youtube_analytics, channel_instance):
        video_request = youtube.search().list(part="snippet", channelId=channel_instance.channel_id, maxResults=50, order="date")
        video_response = video_request.execute()

        for item in video_response['items']:
            video_instance, video_created = YouTubeVideoInformation.objects.get_or_create(
                channel_information=channel_instance,
                video_id=item['id']['videoId'],
                defaults={
                    "title": item['snippet']['title'],
                    "description": item['snippet']['description'],
                    "published_at": item['snippet']['publishedAt'],
                    "thumbnail_url": item['snippet']['thumbnails']['default']['url'],
                }
            )

            if video_created:
                self.update_video_analytics(youtube_analytics, video_instance, channel_instance)

    def update_video_analytics(self, youtube_analytics, video_instance, channel_instance):
        start_date = video_instance.published_at.strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        video_analytics_request = youtube_analytics.reports().query(
            ids=f'channel==MINE',
            startDate=start_date,
            endDate=end_date,
            filters=f'video=={video_instance.video_id}',
            metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares',
            dimensions='day',
            sort='day'
        )
        video_analytics_response = video_analytics_request.execute()

        for row in video_analytics_response.get('rows', []):
            YouTubeVideoAnalytics.objects.update_or_create(
                video_information=video_instance,
                date=datetime.strptime(row[0], '%Y-%m-%d'),
                defaults={
                    'views': row[1],
                    'estimated_minutes_watched': row[2],
                    'average_view_duration': row[3],
                    'likes': row[4],
                    'dislikes': row[5],
                    'comments': row[6],
                    'shares': row[7],
                }
            )

    def update_demographics(self, youtube_analytics, channel_instance, channel_info):
        start_date = channel_info['snippet']['publishedAt'].split("T")[0]
        end_date = datetime.now().strftime("%Y-%m-%d")

        # Update gender demographics
        gender_demographics_request = youtube_analytics.reports().query(
            ids=f'channel=={channel_instance.channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='viewerPercentage',
            dimensions='gender',
            sort='gender'
        )
        gender_demographics_response = gender_demographics_request.execute()

        for row in gender_demographics_response.get('rows', []):
            YouTubeGenderDemographics.objects.update_or_create(
                channel_information=channel_instance,
                date=datetime.now(),
                defaults={
                    'male_percentage': row[1] if row[0] == 'male' else None,
                    'female_percentage': row[1] if row[0] == 'female' else None,
                    'unknown_percentage': row[1] if row[0] == 'unknown' else None,
                }
            )

        # Update age demographics
        age_demographics_request = youtube_analytics.reports().query(
            ids=f'channel=={channel_instance.channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='viewerPercentage',
            dimensions='ageGroup',
            sort='ageGroup'
        )
        age_demographics_response = age_demographics_request.execute()

        for row in age_demographics_response.get('rows', []):
            YouTubeAgeDemographics.objects.update_or_create(
                channel_information=channel_instance,
                date=datetime.now(),
                defaults={f"age_group_{row[0].replace('-', '_')}": row[1]}
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully updated YouTube data for channel {channel_instance.title}"))
