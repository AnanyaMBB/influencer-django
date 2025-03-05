import django_filters
from django.db.models import Q, Max, Sum
from .models import InfluencerAccount
from . import models

class InfluencerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    username = django_filters.CharFilter(method='filter_username')
    followers = django_filters.NumberFilter(method='filter_followers')
    price = django_filters.NumberFilter(method='filter_price')
    location = django_filters.CharFilter(method='filter_location')

    def filter_username(self, queryset, name, value):
        return queryset.filter(
            instagraminitialinformation__username__icontains=value
        ).order_by(
            '-instagraminitialinformation__date'
        ).distinct('instagraminitialinformation__username')

    def filter_followers(self, queryset, name, value):
        return queryset.annotate(
            latest_followers=Max('instagraminitialinformation__followers_count')
        ).filter(
            latest_followers__lte=value
        ).order_by('-latest_followers')

    def filter_price(self, queryset, name, value):
        return queryset.filter(
            Q(baseservice__ugcservice__post_price__lte=value) |
            Q(baseservice__feedpostservice__post_price_per_hour__lte=value) |
            Q(baseservice__storypostservice__post_price_per_hour__lte=value) |
            Q(baseservice__reelpostservice__post_price_per_hour__lte=value) |
            Q(baseservice__otherservice__price__lte=value)
        ).distinct()

    def filter_location(self, queryset, name, value):
        city_queryset = queryset.filter(
            Q(instagramcitydemographics__this_week_city__icontains=value) |
            Q(instagramcitydemographics__this_month_city__icontains=value) |
            Q(instagramcitydemographics__prev_month_city__icontains=value) |
            Q(instagramcitydemographics__last_14_days_city__icontains=value) |
            Q(instagramcitydemographics__last_30_days_city__icontains=value) |
            Q(instagramcitydemographics__last_90_days_city__icontains=value)
        ).annotate(
            follower_count=Sum('instagramcitydemographics__this_week_follower_count') +
                           Sum('instagramcitydemographics__this_month_follower_count') +
                           Sum('instagramcitydemographics__prev_month_follower_count') +
                           Sum('instagramcitydemographics__last_14_days_follower_count') +
                           Sum('instagramcitydemographics__last_30_days_follower_count') +
                           Sum('instagramcitydemographics__last_90_days_follower_count')
        ).order_by('-follower_count')

        country_queryset = queryset.filter(
            Q(instagramcountrydemographics__this_week_country__icontains=value) |
            Q(instagramcountrydemographics__this_month_country__icontains=value) |
            Q(instagramcountrydemographics__prev_month_country__icontains=value) |
            Q(instagramcountrydemographics__last_14_days_country__icontains=value) |
            Q(instagramcountrydemographics__last_30_days_country__icontains=value) |
            Q(instagramcountrydemographics__last_90_days_country__icontains=value)
        ).annotate(
            follower_count=Sum('instagramcountrydemographics__this_week_follower_count') +
                           Sum('instagramcountrydemographics__this_month_follower_count') +
                           Sum('instagramcountrydemographics__prev_month_follower_count') +
                           Sum('instagramcountrydemographics__last_14_days_follower_count') +
                           Sum('instagramcountrydemographics__last_30_days_follower_count') +
                           Sum('instagramcountrydemographics__last_90_days_follower_count')
        ).order_by('-follower_count')

        return city_queryset.union(country_queryset)

    class Meta:
        model = InfluencerAccount
        fields = ['name', 'username', 'followers', 'price', 'location']


class PhylloAccountProfileFilter(django_filters.FilterSet):
    phyllo_account_platform_username = django_filters.CharFilter(lookup_expr="icontains")  # Case-insensitive search
    phyllo_reputation_follower_count = django_filters.RangeFilter()  # Followers range filtering
    phyllo_category = django_filters.CharFilter(lookup_expr="icontains")  # Niche
    country = django_filters.CharFilter(method="filter_by_country")  # Custom filter method
    city = django_filters.CharFilter(method="filter_by_city")  # Custom filter method

    class Meta:
        model = models.PhylloAccountProfile
        fields = ["phyllo_account_platform_username", "phyllo_reputation_follower_count", "phyllo_category"]

    def filter_by_country(self, queryset, name, value):
        """Filter profiles based on audience country demographics."""
        return queryset.filter(
            phyllo_account__phylloaddedaccounts__phylloaudiencedemographics__country_demographics__country_code__icontains=value
        )

    def filter_by_city(self, queryset, name, value):
        """Filter profiles based on audience city demographics."""
        return queryset.filter(
            phyllo_account__phylloaddedaccounts__phylloaudiencedemographics__city_demographics__city__icontains=value
        )