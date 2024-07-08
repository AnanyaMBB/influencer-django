from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import (
    InfluencerAccount,
    InfluencerInstagramInformation,
    InstagramInitialInformation,
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
    help = "Download data from Instagram API and store it in the database"

    def handle(self, *args, **options):
        self.stdout.write("Starting Instagram data update...")
        self.get_data()

    def get_data(self):
        timeframes = [
            "this_week",
            "this_month",
            "prev_month",
            "last_14_days",
            "last_30_days",
            "last_90_days",
        ]

        ages = ["_13_17", "_18_24", "_25_34", "_35_44", "_45_54", "_55_64", "_65"]
        genders = ["_male", "_female", "_unknown"]
        demographicsDataBreakdowns = ["age", "gender", "city", "country"]
        demographicsDataTypes = [
            "follower_demographics",
            "engaged_audience_demographics",
            "reached_audience_demographics",
        ]

        initialInformations = [
            "name",
            "username",
            "profile_picture_url",
            "biography",
            "followers_count",
            "follows_count",
            "media_count",
            "website",
        ]

        detailsString = "likes,comments,saves,shares,profile_views,replies,profile_links_taps,website_clicks,profile_views,impressions,reach,total_interactions,accounts_engaged"

        date = datetime.now()
        date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        influencerAccounts = InfluencerAccount.objects.all()
        for influencerAccount in influencerAccounts:
            influencerInstagramInformations = (
                InfluencerInstagramInformation.objects.filter(
                    influencer=influencerAccount
                )
            )

            # Get Instagram Initial Information
            if len(influencerInstagramInformations) < 1:
                continue
            for influencerInstagramInformation in influencerInstagramInformations:
                try:
                    self.getInitialInformation(
                        influencerInstagramInformation, date, initialInformations
                    )
                except Exception as e:
                    print("Error in Instagram Initial Information", e)

                # Get Instagram Details
                try:
                    self.getDetails(influencerInstagramInformation, date, detailsString)
                except Exception as e:
                    print("Error in Instagram Details", e)

                # Get Demographics Data
                for breakdown in demographicsDataBreakdowns:
                    for dataTypeIdentifier, dataType in enumerate(
                        demographicsDataTypes
                    ):
                        for timeframe in timeframes:
                            if breakdown == "age":
                                try:
                                    self.getDemographicsData(
                                        influencerInstagramInformation,
                                        date,
                                        timeframe,
                                        breakdown,
                                        dataTypeIdentifier,
                                        dataType,
                                        ages,
                                    )
                                except Exception as e:
                                    print("Error in age demographics", e)

                            elif breakdown == "gender":
                                try:
                                    self.getDemographicsData(
                                        influencerInstagramInformation,
                                        date,
                                        timeframe,
                                        breakdown,
                                        dataTypeIdentifier,
                                        dataType,
                                        genders,
                                    )
                                except Exception as e:
                                    print("Error in gender demographics", e)
                            elif breakdown == "city":
                                try:
                                    self.getDemographicsData(
                                        influencerInstagramInformation,
                                        date,
                                        timeframe,
                                        breakdown,
                                        dataTypeIdentifier,
                                        dataType,
                                        None,
                                    )
                                except Exception as e:
                                    print("Error in city demographics", e)
                            elif breakdown == "country":
                                try:
                                    self.getDemographicsData(
                                        influencerInstagramInformation,
                                        date,
                                        timeframe,
                                        breakdown,
                                        dataTypeIdentifier,
                                        dataType,
                                        None,
                                    )
                                except Exception as e:
                                    print("Error in country demographics", e)
                # Get Media Data
                try:
                    self.getMediaData(influencerInstagramInformation, date)
                except Exception as e:
                    print("Error in Media Data", e)

    def getInitialInformation(
        self, influencerInstagramInformation, date, initialInformations
    ):
        access_token = influencerInstagramInformation.long_access_token
        facebookApiRequest = requests.get(
            f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}"
            f"?fields=name,username,profile_picture_url,biography,followers_count,follows_count,media_count,website"
            f"&access_token={access_token}"
        )

        instagramInitialInformation, _ = (
            InstagramInitialInformation.objects.get_or_create(
                influencer_instagram_information=influencerInstagramInformation,
                date=date,
            )
        )
        for initialInformation in initialInformations:
            if initialInformation in facebookApiRequest.json():
                setattr(
                    instagramInitialInformation,
                    initialInformation,
                    (facebookApiRequest.json()[initialInformation]),
                )
        instagramInitialInformation.save()

    def getDetails(self, influencerInstagramInformation, date, detailsString):
        access_token = influencerInstagramInformation.long_access_token
        facebookApiRequest = requests.get(
            f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}/"
            f"insights?metric={detailsString}"
            f"&period=day"
            f"&metric_type=total_value"
            f"&access_token={access_token}"
        )

        instagramDetail, _ = InstagramDetails.objects.get_or_create(
            influencer_instagram_information=influencerInstagramInformation,
            date=date,
        )
        if "data" in facebookApiRequest.json():
            for result in facebookApiRequest.json()["data"]:
                setattr(instagramDetail, result["name"], result["total_value"]["value"])
        instagramDetail.save()

    def getDemographicsData(
        self,
        influencerInstagramInformation,
        date,
        timeframe,
        breakdown,
        dataTypeIdentifier,
        dataType,
        dataValues,
    ):
        access_token = influencerInstagramInformation.long_access_token
        if breakdown == "age":
            facebookApiRequest = requests.get(
                f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}/"
                f"insights?metric={dataType}"
                f"&period=lifetime"
                f"&timeframe={timeframe}"
                f"&breakdown=age"
                f"&metric_type=total_value"
                f"&access_token={access_token}"
            )

            instagramAgeDemographics, _ = (
                InstagramAgeDemographics.objects.get_or_create(
                    influencer_instagram_information=influencerInstagramInformation,
                    date=date,
                    type_identifier=dataTypeIdentifier,
                )
            )
            if "error" in facebookApiRequest.json():
                return
            for result, age in zip(
                facebookApiRequest.json()["data"][0]["total_value"]["breakdowns"][0][
                    "results"
                ],
                dataValues,
            ):

                setattr(instagramAgeDemographics, timeframe + age, result["value"])
            instagramAgeDemographics.save()

        elif breakdown == "gender":
            facebookApiRequest = requests.get(
                f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}/"
                f"insights?metric={dataType}"
                f"&period=lifetime"
                f"&timeframe={timeframe}"
                f"&breakdown=gender"
                f"&metric_type=total_value"
                f"&access_token={access_token}"
            )

            if "error" in facebookApiRequest.json():
                return

            instagramGenderDemographics, _ = (
                InstagramGenderDemographics.objects.get_or_create(
                    influencer_instagram_information=influencerInstagramInformation,
                    date=date,
                    type_identifier=dataTypeIdentifier,
                )
            )

            for result, gender in zip(
                facebookApiRequest.json()["data"][0]["total_value"]["breakdowns"][0][
                    "results"
                ],
                dataValues,
            ):

                setattr(
                    instagramGenderDemographics, timeframe + gender, result["value"]
                )
            instagramGenderDemographics.save()

        elif breakdown == "city":
            facebookApiRequest = requests.get(
                f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}/"
                f"insights?metric={dataType}"
                f"&period=lifetime"
                f"&timeframe={timeframe}"
                f"&breakdown=city"
                f"&metric_type=total_value"
                f"&access_token={access_token}"
            )

            if "error" in facebookApiRequest.json():
                return

            for count, result in enumerate(
                facebookApiRequest.json()["data"][0]["total_value"]["breakdowns"][0][
                    "results"
                ]
            ):
                instagramCityDemographics, _ = (
                    InstagramCityDemographics.objects.get_or_create(
                        influencer_instagram_information=influencerInstagramInformation,
                        count=count,
                        date=date,
                        type_identifier=dataTypeIdentifier,
                    )
                )

                setattr(
                    instagramCityDemographics,
                    timeframe + "_city",
                    result["dimension_values"],
                )
                setattr(
                    instagramCityDemographics,
                    timeframe + "_follower_count",
                    result["value"],
                )
                instagramCityDemographics.save()

        elif breakdown == "country":
            facebookApiRequest = requests.get(
                f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}/"
                f"insights?metric={dataType}"
                f"&period=lifetime"
                f"&timeframe={timeframe}"
                f"&breakdown=country"
                f"&metric_type=total_value"
                f"&access_token={access_token}"
            )

            if "error" in facebookApiRequest.json():
                return

            for count, result in enumerate(
                facebookApiRequest.json()["data"][0]["total_value"]["breakdowns"][0][
                    "results"
                ]
            ):
                instagramCountryDemographics, _ = (
                    InstagramCountryDemographics.objects.get_or_create(
                        influencer_instagram_information=influencerInstagramInformation,
                        count=count,
                        date=date,
                        type_identifier=dataTypeIdentifier,
                    )
                )

                setattr(
                    instagramCountryDemographics,
                    timeframe + "_country",
                    result["dimension_values"][0],
                )
                setattr(
                    instagramCountryDemographics,
                    timeframe + "_follower_count",
                    result["value"],
                )
                instagramCountryDemographics.save()

    def getMediaData(self, influencerInstagramInformation, date):
        fields_media = [
            str(field).split(".")[-1]
            for field in InstagramMediaData._meta.get_fields()[2:]
        ]

        fields_comment = [
            str(field).split(".")[-1]
            for field in InstagramMediaComment._meta.get_fields()[2:]
        ]

        fields_media.remove("media_id")
        fields_media.remove("date")

        print(f"Fields Media: {fields_media}")

        fields_comment.remove("media_id")
        fields_comment.remove("comment_id")
        fields_comment.remove("date")

        access_token = influencerInstagramInformation.long_access_token

        facebookApiRequest = requests.get(
            f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}/media?access_token={access_token}"
        )

        for media in facebookApiRequest.json()["data"]:
            facebookApiRequestField = requests.get(
                f'https://graph.facebook.com/v18.0/{media["id"]}?fields=media_url,caption,id,timestamp,is_comment_enabled,is_shared_to_feed,like_count,media_product_type,media_type,thumbnail_url,comments_count&access_token={access_token}'
            )

            facebookApiRequestComment = requests.get(
                f'https://graph.facebook.com/v18.0/{media["id"]}/comments?access_token={access_token}'
            )

            if facebookApiRequestField.json()["media_type"] == "REELS":
                facebookApiRequestInsight = requests.get(
                    f'https://graph.facebook.com/v18.0/{media["id"]}/insights?metric=impressions,shares,reach,saved,video_views,total_interactions,profile_activity,profile_visits,ig_reels_avg_watch_time,ig_reels_video_view_total_time,plays&access_token={access_token}'
                )
            else:
                facebookApiRequestInsight = requests.get(
                    f'https://graph.facebook.com/v18.0/{media["id"]}/insights?metric=impressions,reach,shares,saved,video_views,total_interactions,profile_activity,profile_visits&access_token={access_token}'
                )

            if (
                "error" in facebookApiRequestInsight.json()
                or "error" in facebookApiRequestField.json()
            ):
                continue
            
            extractedInsight = {
                item["name"]: item["values"][0]["value"]
                for item in facebookApiRequestInsight.json()["data"]
            }
            combinedData = {**dict(facebookApiRequestField.json()), **extractedInsight}
            update_fields = {}
            for field in fields_media:
                if field in combinedData:
                    print(f"Field: {field} : {combinedData[field]}")
                    update_fields[field] = combinedData[field]
                else:
                    if field != 'instagrammediacomment>':
                        print(f"Field: {field} : None")
                        update_fields[field] = None

            instagramMediaData, created = InstagramMediaData.objects.update_or_create(
                influencer_instagram_information=influencerInstagramInformation,
                date=date,
                media_id=media["id"],
                defaults=update_fields
            )

            # instagramMediaData, created = InstagramMediaData.objects.get_or_create(
            #     influencer_instagram_information=influencerInstagramInformation,
            #     date=date,
            #     media_id=media["id"],
            # )

            

            # extractedInsight = {
            #     item["name"]: item["values"][0]["value"]
            #     for item in facebookApiRequestInsight.json()["data"]
            # }
            # combinedData = {**dict(facebookApiRequestField.json()), **extractedInsight}

            # for field in fields_media:
            #     if field in combinedData:  
            #         setattr(instagramMediaData, field, combinedData[field])
            #     else:
            #         setattr(instagramMediaData, field, None)

            # instagramMediaData.save()
            
            

            for comment in facebookApiRequestComment.json()["data"]:
                facebookApiRequestCommentInsight = requests.get(
                    f'https://graph.facebook.com/v18.0/{comment["id"]}?fields=id,timestamp,text,parent_id,like_count,hidden,username,user&access_token={access_token}'
                )
                instagramMediaComment, _ = InstagramMediaComment.objects.get_or_create(
                    media_id=instagramMediaData,
                    influencer_instagram_information=influencerInstagramInformation,
                    date=date,
                    comment_id=comment["id"],
                )

                for field in fields_comment:
                    if field in facebookApiRequestCommentInsight.json():
                        setattr(
                            instagramMediaComment,
                            field,
                            facebookApiRequestCommentInsight.json()[field],
                        )
                    else:
                        setattr(instagramMediaComment, field, None)
                instagramMediaComment.save()

                print(f"Comment: {comment}")
