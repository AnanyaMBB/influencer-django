from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import base64
import requests


scheduler_instance = BackgroundScheduler()
scheduler_instance.start()


def publish_post(account_id, title, description, type, visibility, retry, media_media_type, media_source_media_url, media_source_thumbnail_url, media_thumbnail_offset, media_additional_info): 
    credentials = "70a4fab4-8f91-443a-9330-3349431b5029:e140a14a-788d-4ec0-b0df-d34a8aced66a"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    url = "https://api.staging.insightiq.ai/v1/social/contents/publish"
    payload = {
        "account_id": account_id, 
        "title": title,
        "type": type,
        "visibility": visibility,
        "retry": retry,
        "media": {
            "media_type": media_media_type,
            "source_media_url": media_source_media_url,
            # "source_thumbnail_url": media_source_thumbnail_url,
            # "thumbnail_offset": media_thumbnail_offset,
            # "additional_info": media_additional_info
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

def add_job_to_scheduler(post):
    scheduler_instance.add_job(
        publish_post,
        'date',
        run_date=post.scheduled_time,
        args=[post.account_id, post.title, post.description, post.type, post.visiblity, post.retry, post.media_media_type, post.media_source_media_url, post.media_thumbnail_offset, post.media_additional_info],
        id=f"post_{post.id}"
    )