import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Uploads a video to YouTube'

    def add_arguments(self, parser):
        parser.add_argument('video_file', type=str, help='Path to the video file')
        parser.add_argument('title', type=str, help='Title of the video')
        parser.add_argument('description', type=str, help='Description of the video')
        parser.add_argument('--tags', type=str, nargs='+', default=[], help='Tags for the video')
        parser.add_argument('--category', type=str, default='22', help='Category ID for the video (default: "People & Blogs")')
        parser.add_argument('--privacy', type=str, default='public', choices=['public', 'private', 'unlisted'], help='Privacy status of the video')

    def handle(self, *args, **kwargs):
        video_file = kwargs['video_file']
        title = kwargs['title']
        description = kwargs['description']
        tags = kwargs['tags']
        category = kwargs['category']
        privacy_status = kwargs['privacy']

        # Path to the credentials JSON file you downloaded
        credentials_file = './client_secret.json'

        # Load credentials from file
        creds = None
        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as file:
                creds_data = json.load(file)
                creds = Credentials.from_authorized_user_info(info=creds_data)

        # If credentials are expired, refresh them
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        if not creds:
            raise CommandError("Failed to load credentials")

        # Build the YouTube API client
        youtube = build("youtube", "v3", credentials=creds)

        # Prepare the video metadata
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category,
            },
            "status": {
                "privacyStatus": privacy_status,
            }
        }

        # Specify the video file to upload
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)

        # Make the request to the YouTube API
        try:
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            response = request.execute()
            
            self.stdout.write(self.style.SUCCESS(f"Video uploaded successfully! Video ID: {response.get('id')}"))
        except Exception as e:
            raise CommandError(f"Failed to upload video: {str(e)}")
