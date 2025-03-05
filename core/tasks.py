from celery import shared_task
from django.utils import timezone
from .models import PhylloScheduledPost
from . import models 
import base64
import requests
import urllib.parse 
from datetime import datetime
from django.utils.dateparse import parse_datetime

@shared_task
def publish_scheduled_posts():
    now = timezone.now()
    print("now: ", now) 
    due_posts = PhylloScheduledPost.objects.filter(
        scheduled_time__lte=now,
        status="DBSAVED",
        business_accepted=True, 
        influencer_accepted=True,
        business_contract_signed=True, 
        influencer_contract_signed=True, 
        payment_completed=True, 
    )
    print("due posts: ", due_posts)
    
    for post in due_posts:
        try: 
            credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            url = "https://api.staging.insightiq.ai/v1/social/contents/publish"
            encoded_media_url = urllib.parse.quote(
                post.media_source_media_url,
                safe=':/?=&'
            )
            payload = {
                "account_id": post.phyllo_account.phyllo_accountid,
                "title": post.title,
                "type": post.type,
                "visibility": post.visibility,
                "retry": post.retry,
                "media": [{
                    "media_type": post.media_media_type,
                    "source_media_url": encoded_media_url,
                    # "source_thumbnail_url": media_source_thumbnail_url,
                    # "thumbnail_offset": media_thumbnail_offset,
                    # "additional_info": media_additional_info
                }]
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_credentials}"
            }

            response = requests.post(url, json=payload, headers=headers)
            if  'error' in response.json():
                print(response.json())
                raise Exception("Failed to post scheduled post")
            
            post.status = "POSTED"
            print("==============================================")
            print(response.json()['data'])
            print(response.json()['data']['id'])
            post.publish_id = response.json()['data']["id"]
            post.save()
            print(response.json())
            print("==============================================")
            print("Successfully posted scheduled post")

            url = "https://api.staging.insightiq.ai/v1/webhooks"
            payload = {
                "url": "https://fdcd-79-110-55-8.ngrok-free.app/api/campaign/published/success/webhook",
                "events": [
                    "CONTENTS.PUBLISH_SUCCESS",
                ],
                "name": "publish webhook"
            }
            response = requests.post(url, json=payload, headers=headers)
            print("*** webhook response ***")
            print(response.json())
            print("************************")
        except Exception as e: 
            print(f"Error posting scheduled post: {e}")
            post.status = "FAILED"
            post.save()


@shared_task
def grab_published_analytics(): 
    due_posts = PhylloScheduledPost.objects.filter(
        status="POSTED",
        business_accepted=True, 
        influencer_accepted=True,
        business_contract_signed=True, 
        influencer_contract_signed=True, 
        payment_completed=True, 
        final_status="SUCCESS"
    )
    print("get analytics posts: ", due_posts)

    for post in due_posts:
        try:          
            contentData = getContentData(post.content_id)
            print("Content Data: ", contentData)
            if contentData: 
                phylloPostedContentData = models.PhylloPostedContentData(
                    phyllo_scheduled_post = post,
                    phyllo_contentid = post.content_id, 
                    phyllo_created_at = parse_datetime(contentData.get("created_at", None)) if contentData.get("created_at") else None, 
                    phyllo_updated_at = parse_datetime(contentData.get("updated_at", None)) if contentData.get("updated_at") else None,
                    phyllo_user_id = contentData.get("user", {}).get("id", None),
                    phyllo_user_name = contentData.get("user", {}).get("name", None),
                    phyllo_accountid = contentData.get("account", {}).get("id", None),
                    phyllo_account_platform_username = contentData.get("account", {}).get("platform_username", None),
                    phyllo_work_platform_id = contentData.get("work_platform", {}).get("id", None),
                    phyllo_work_platform_name = contentData.get("work_platform", {}).get("name", None),
                    phyllo_work_platform_logo_url = contentData.get("work_platform", {}).get("logo_url", None),
                    phyllo_engagement_like_count = contentData.get("engagement", {}).get("like_count", None),
                    phyllo_engagement_dislike_count = contentData.get("engagement", {}).get("dislike_count", None), 
                    phyllo_engagement_comment_count = contentData.get("engagement", {}).get("comment_count", None),
                    phyllo_engagement_impression_organic_count = contentData.get("engagement", {}).get("impression_organic_count", None),
                    phyllo_engagement_reach_organic_count = contentData.get("engagement", {}).get("reach_organic_count", None),
                    phyllo_engagement_save_count = contentData.get("engagement", {}).get("save_count", None),
                    phyllo_engagement_view_count = contentData.get("engagement", {}).get("view_count", None),
                    phyllo_engagement_watch_time_in_hours = contentData.get("engagement", {}).get("watch_time_in_hours", None),
                    phyllo_engagement_share_count = contentData.get("engagement", {}).get("share_count", None),
                    phyllo_engagement_impression_paid_count = contentData.get("engagement", {}).get("impression_paid_count", None),
                    phyllo_engagement_reach_paid_count = contentData.get("engagement", {}).get("reach_paid_count", None),
                    phyllo_external_id = contentData.get("external_id", None),
                    phyllo_title = contentData.get("title", None),
                    phyllo_format = contentData.get("format", None),
                    phyllo_type = contentData.get("type", None),
                    phyllo_url = contentData.get("url", None),
                    phyllo_media_url = contentData.get("media_url", None),
                    phyllo_duration = contentData.get("duration", None),
                    phyllo_description = contentData.get("description", None),
                    phyllo_visibility = contentData.get("visibility", None),
                    phyllo_thumbnail_url = contentData.get("thumbnail_url", None),
                    phyllo_published_at = contentData.get("published_at", None),
                    phyllo_platform_profile_id = contentData.get("platform_profile_id", None),
                    phyllo_platform_profile_name = contentData.get("platform_profile_name", None),
                    phyllo_sponsored = contentData.get("sponsored", None),
                    phyllo_collaboration = contentData.get("collaboration", None),
                )

                phylloPostedContentData.save()
            
            comments = getComments(post.phyllo_account.phyllo_accountid, post.content_id)
            print("Comments: ", comments)
            if comments: 
                for comment in comments["data"]:
                    phylloPostedComments = models.PhylloPostedComments(
                        phyllo_scheduled_post = post, 
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
                    phylloPostedComments.save()

            

        except Exception as e:
            print("Error grabbing published analytics: ", e)


def getContentData(content_id): 
    try: 
        # https://api.staging.insightiq.ai/v1/social/contents/7466102213845257479
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        url = f"https://api.staging.insightiq.ai/v1/social/contents/{content_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e: 
        print(f"Error getting content data: {e}")
        return None
    
def getComments(account_id, content_id): 
    try: 
        url = "https://api.staging.insightiq.ai/v1/social/comments"
        querystring = {"account_id":account_id,"content_id":content_id}
        credentials = "d1c95dc7-0ad9-4db3-8530-14b33ed91842:6eb3551e-db1a-4f5f-acbc-fb8f91dbc936"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        response = requests.get(url, headers=headers, params=querystring)

        return response.json()
    except Exception as e:
        print(f"Error getting comments: {e}")
        return None
    

def getAudienceDemographics(): 
    pass

