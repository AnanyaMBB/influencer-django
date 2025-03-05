from django.core.management.base import BaseCommand 
from django.utils import timezone 
from core import models 
from tikapi import TikAPI, ValidationException, ResponseException 

api = TikAPI("N1S5fCcqeBIn58vAMjjD5G6z8LlbcTs3pbbeh5msh0W7r13V")

class Command(BaseCommand): 
    help = "Get TikTok Data"

    def handle(self, *args, **kwargs): 
        self.stdout.write("Getting TikTok Data")
        self.getTikTokInformation() 

    def getTikTokInformation(self): 
        try: 
            tiktokAccount = models.TikTokAccount.objects.all()
            for account in tiktokAccount: 
                user = api.user(accountKey=account.tiktok_access_token)
                response = user.info()
                response = response.json()

                tiktokAccountInformation, created = models.TikTokAccountInformation.objects.update_or_create(
                    tiktok_account=account,  # Unique identifier for the entry
                    defaults={
                        'tiktok_unique_id': response["userInfo"]["user"]["uniqueId"],
                        'tiktok_sec_uid': response["userInfo"]["user"]["secUid"],
                        'tiktok_nickname': response["userInfo"]["user"]["nickname"],
                        'tiktok_avatar': response["userInfo"]["user"]["avatarLarger"],
                        'tiktok_signature': response["userInfo"]["user"]["signature"],
                        'tiktok_digg_count': response["userInfo"]["stats"]["diggCount"],
                        'tiktok_follower_count': response["userInfo"]["stats"]["followerCount"],
                        'tiktok_following_count': response["userInfo"]["stats"]["followingCount"],
                        'tiktok_friend_count': response["userInfo"]["stats"]["friendCount"],
                        'tiktok_heart': response["userInfo"]["stats"]["heartCount"],
                        'tiktok_video_count': response["userInfo"]["stats"]["videoCount"],
                        'tiktok_verified': response["userInfo"]["user"]["verified"] == "true",
                    }
                )

            if created:
                print("A new entry was created.")
            else:
                print("The entry was updated.")

        except ValidationException as e: 
            print(e, e.field)

        except ResponseException as e: 
            print(e, e.response.status_code)

    
