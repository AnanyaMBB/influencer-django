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

        influencerAccounts = InfluencerAccount.objects.all()
        for influencerAccount in influencerAccounts:
            influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
                influencer=influencerAccount
            )

            # Get Instagram Initial Information
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
                for dataTypeIdentifier, dataType in enumerate(demographicsDataTypes):
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

    def getInitialInformation(
        self, influencerInstagramInformation, date, initialInformations
    ):
        access_token = influencerInstagramInformation.long_access_token
        facebookApiRequest = requests.get(
            f"https://graph.facebook.com/v18.0/{influencerInstagramInformation.instagram_id}"
            f"?fields=name,username,profile_picture_url,biography,followers_count,follows_count,media_count,website"
            f"&access_token=${access_token}"
        )

        instagramInitialInformation, _ = (
            InstagramInitialInformation.objects.get_or_create(
                influencer_instagram_information=influencerInstagramInformation,
                date=date,
            )
        )
        for initialInformation in initialInformations:
            setattr(
                instagramInitialInformation,
                initialInformation,
                facebookApiRequest.json()[initialInformation],
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

        instagramDetail = InstagramDetails.objects.get_or_create(
            influencer_instagram_information=influencerInstagramInformation,
            date=date,
        )
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

            instagramCityDemographics, _ = (
                InstagramCityDemographics.objects.get_or_create(
                    influencer_instagram_information=influencerInstagramInformation,
                    date=date,
                    type_identifier=dataTypeIdentifier,
                )
            )

            for count, result in enumerate(
                facebookApiRequest.json()["data"][0]["total_value"]["breakdowns"][0][
                    "results"
                ]
            ):

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

            instagramCountryDemographics, _ = (
                InstagramCountryDemographics.objects.get_or_create(
                    influencer_instagram_information=influencerInstagramInformation,
                    date=date,
                    type_identifier=dataTypeIdentifier,
                )
            )
            for count, result in enumerate(
                facebookApiRequest.json()["data"][0]["total_value"]["breakdowns"][0][
                    "results"
                ]
            ):

                setattr(
                    instagramCountryDemographics,
                    timeframe + "_country",
                    result["dimension_values"],
                )
                setattr(
                    instagramCountryDemographics,
                    timeframe + "_follower_count",
                    result["value"],
                )
            instagramCountryDemographics.save()
