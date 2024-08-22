import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.errors

# Assuming you have these tokens stored in your database
ACCESS_TOKEN = 'ya29.a0AcM612w25lWVoJyxpD2t1unN1BY-kbyTQroQODvd-JFq5ORQ5loXRSpiWVls8lF1d0fPLJI3RoXVPKg8kM0-mhRSihO4ZJKP2r9he41hckrCWOgqSfeAefuAo757OI8AYGO0bKMgl8hXslF_QRQooeHYFApJXtzZ1c_9aCgYKAfcSARESFQHGX2MiWlnK7NX0zdq9J2pJ-aZtNw0171'
REFRESH_TOKEN = '1//0e_SAueY5G_IcCgYIARAAGA4SNwF-L9IrqNO0Ww0TwvFbzGd2gVOTBIoz5o1k0rPAsI24obGkWv8bKUXsVMvIuGvAlSOUuFcuCg0'
CLIENT_ID = ' 119904184627-1ssstt91tkt1lj9lda9e5hb4oi9kiqdo.apps.googleusercontent.com'
CLIENT_SECRET = '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'
TOKEN_URI = 'https://oauth2.googleapis.com/token'

# Construct the credentials object
credentials = google.oauth2.credentials.Credentials(
    token=ACCESS_TOKEN,
    refresh_token=REFRESH_TOKEN,
    token_uri=TOKEN_URI,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Refresh the token if needed
request = google.auth.transport.requests.Request()
credentials.refresh(request)

# Initialize the YouTube API client
youtube = googleapiclient.discovery.build(
    'youtube', 'v3', credentials=credentials)

def upload_video(service):
    request_body = {
        "snippet": {
            "categoryId": "22",  # Category ID for People & Blogs
            "title": "Smart Chain Video",
            "description": "test",
            "tags": ["tag1", "tag2"]
        },
        "status": {
            "privacyStatus": "public"  # or "private" or "unlisted"
        }
    }

    media = googleapiclient.http.MediaFileUpload("./video.mp4", chunksize=-1, resumable=True)

    response = service.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    ).execute()

    print(f"Video uploaded. Video ID: {response['id']}")

if __name__ == "__main__":
    try:
        upload_video(youtube)
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error occurred: {e.resp.status} - {e.content}")
