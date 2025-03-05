import requests
import base64

# Replace with your actual credentials and TikTok-specific values
username = "70a4fab4-8f91-443a-9330-3349431b5029"
password = "your_password_here"
account_id = "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65"

# Base64 encode the username:password
credentials = f"{username}:{password}"
auth_header = base64.b64encode(credentials.encode()).decode()

# API Endpoint
url = "https://api.sandbox.insightiq.ai/v1/social/contents/publish"

# Payload for the TikTok post
payload = {
    "account_id": account_id,
    "title": "My first TikTok post!",
    "description": "Check out this amazing video!",
    "type": "VIDEO",  # TikTok uses video content, so the correct type is VIDEO
    "visibility": "PUBLIC",
    "retry": True,  # Enable retry for asynchronous handling
    "additional_info": {},
    "media": [
        {
            "media_type": "VIDEO",
            "source_media_url": "https://example.com/my_video.mp4",  # Publicly accessible video URL
            "thumbnail_offset": 0,  # Offset in milliseconds for thumbnail
            "additional_info": {}
        }
    ]
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {auth_header}"
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Handle response
if response.status_code == 202:
    print("Post request is being processed:", response.json())
elif response.status_code == 200:
    print("Post published successfully:", response.json())
else:
    print(f"Failed to publish post. Status Code: {response.status_code}")
    print("Response:", response.json())







from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import requests
import base64

# Function to publish the post
def publish_post(account_id, title, description, video_url, auth_header):
    url = "https://api.sandbox.insightiq.ai/v1/social/contents/publish"
    payload = {
        "account_id": account_id,
        "title": title,
        "description": description,
        "type": "VIDEO",
        "visibility": "PUBLIC",
        "retry": True,
        "additional_info": {},
        "media": [
            {
                "media_type": "VIDEO",
                "source_media_url": video_url,
                "thumbnail_offset": 0,
                "additional_info": {}
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {auth_header}"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 202:
        print("Post request is being processed:", response.json())
    elif response.status_code == 200:
        print("Post published successfully:", response.json())
    else:
        print(f"Failed to publish post. Status Code: {response.status_code}")
        print("Response:", response.json())

# Scheduler configuration
scheduler = BackgroundScheduler()

# Function to schedule a post
def schedule_post(account_id, title, description, video_url, scheduled_time, auth_header):
    job = scheduler.add_job(
        publish_post,
        'date',
        run_date=scheduled_time,
        args=[account_id, title, description, video_url, auth_header]
    )
    print(f"Scheduled job {job.id} to run at {scheduled_time}")

# Example usage
if __name__ == "__main__":
    # User details and credentials
    username = "70a4fab4-8f91-443a-9330-3349431b5029"
    password = "your_password_here"
    account_id = "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65"
    video_url = "https://example.com/my_video.mp4"
    title = "Scheduled TikTok Post!"
    description = "Check out this amazing scheduled video!"
    credentials = f"{username}:{password}"
    auth_header = base64.b64encode(credentials.encode()).decode()

    # Start the scheduler
    scheduler.start()

    # Schedule the post
    scheduled_time = datetime.now() + timedelta(minutes=5)  # Schedule for 5 minutes from now
    schedule_post(account_id, title, description, video_url, scheduled_time, auth_header)

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()









from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class ScheduledPost(models.Model):
    account_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    scheduled_time = models.DateTimeField()  # Date and time for scheduling
    status = models.CharField(max_length=50, default="scheduled")  # Track the status of the post

# Function to add a new job to the scheduler dynamically
def add_job_to_scheduler(post):
    from apscheduler.schedulers.background import BackgroundScheduler
    from datetime import datetime
    import base64

    # Initialize scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Function to publish the post
    def publish_post(account_id, title, description, video_url):
        print(f"Post published: {title} at {datetime.now()}")

    # Add the post to the scheduler
    scheduler.add_job(
        publish_post,
        'date',
        run_date=post.scheduled_time,
        args=[post.account_id, post.title, post.description, post.video_url],
        id=f"post_{post.id}"  # Unique job ID
    )

# Signal to detect new or updated ScheduledPost entries
@receiver(post_save, sender=ScheduledPost)
def handle_new_post(sender, instance, created, **kwargs):
    if created and instance.scheduled_time > datetime.now():
        add_job_to_scheduler(instance)
