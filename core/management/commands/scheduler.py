from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
import base64
import requests
import time

class Command(BaseCommand):
    help = "Runs APScheduler and schedules jobs for posts."

    def handle(self, *args, **kwargs):
        self.scheduler_instance = BackgroundScheduler()
        self.scheduler_instance.start()
        print("✅ Scheduler started.")

        try:
            while True:
                time.sleep(10)  # Prevents high CPU usage
                self.list_scheduled_jobs()  # Periodically list jobs
        except (KeyboardInterrupt, SystemExit):
            print("Scheduler stopped.")
            self.scheduler_instance.shutdown(wait=False)

    def publish_post(self, account_id, title, description, type, visibility, retry, media_media_type, media_source_media_url, media_source_thumbnail_url, media_thumbnail_offset, media_additional_info):
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
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
                "source_thumbnail_url": media_source_thumbnail_url,
                "thumbnail_offset": media_thumbnail_offset,
                "additional_info": media_additional_info
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        response = requests.post(url, json=payload, headers=headers)
        print(f"Post response: {response.json()}")

    def add_job_to_scheduler(self, post):
        """Schedules a new post"""
        job_id = f"post_{post.id}"
        self.scheduler_instance.add_job(
            self.publish_post,
            'date',
            run_date=post.scheduled_time,
            args=[
                post.account_id, post.title, post.description, post.type, post.visibility,
                post.retry, post.media_media_type, post.media_source_media_url,
                post.media_source_thumbnail_url, post.media_thumbnail_offset,
                post.media_additional_info
            ],
            id=job_id
        )
        print(f"✅ Job scheduled: {job_id}, Scheduled Time: {post.scheduled_time}")

    def list_scheduled_jobs(self):
        """Prints all scheduled jobs"""
        jobs = self.scheduler_instance.get_jobs()
        if not jobs:
            print("📌 No jobs currently scheduled.")
        else:
            print("📅 Scheduled Jobs:")
            for job in jobs:
                print(f"   - Job ID: {job.id}, Next Run: {job.next_run_time}")
