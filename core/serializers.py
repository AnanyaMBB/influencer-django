from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    BusinessAccount,
    InfluencerAccount,
    InfluencerInstagramInformation,
    BaseService,
    UGCService,
    FeedPostService,
    StoryPostService,
    ReelPostService,
    OtherService,
    InstagramBase,
    InstagramInitialInformation,
    InstagramDetails,
    InstagramGenderDemographics,
    InstagramAgeDemographics,
    InstagramCityDemographics,
    InstagramCountryDemographics,
    InstagramMediaData,
    InstagramMediaComment,
    Contract,
    ContractVersion,
    ContractUserPermissions,
    ContractVersionUserPermissions,
    SignatureRequests,
    Files,
    Service,
    ServicePricing,
    Requests,
)

from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class businessAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAccount
        # fields = '__all__'
        exclude = ["user"]


class RegisterSerializer(serializers.ModelSerializer):
    businessAccount = businessAccountSerializer()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "businessAccount",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        business_data = validated_data.pop("businessAccount")
        user = User.objects.create_user(**validated_data)
        BusinessAccount.objects.create(user=user, **business_data)
        return user


class InfluencerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerAccount
        exclude = ["user"]


class InfluencerRegisterSerializer(serializers.ModelSerializer):
    influencerAccount = InfluencerAccountSerializer()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "influencerAccount",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        influencer_data = validated_data.pop("influencerAccount")
        user = User.objects.create_user(**validated_data)
        InfluencerAccount.objects.create(user=user, **influencer_data)
        return user


class InstagramInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerInstagramInformation
        fields = "__all__"


class InfluencerInstagramInformationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)

    class Meta:
        model = InfluencerInstagramInformation
        exclude = ["influencer"]

    def create(self, validated_data):
        user = User.objects.get(username=validated_data["user"])
        validated_data.pop("user")
        influencer = InfluencerAccount.objects.get(user=user)
        return InfluencerInstagramInformation.objects.create(
            influencer=influencer, **validated_data
        )


class InfluencerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerInstagramInformation
        fields = "__all__"


class BaseServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)

    class Meta:
        model = BaseService
        exclude = ["instagram_information"]

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(
            instagram_id=validated_data["instagram_id"]
        )
        validated_data.pop("instagram_id")
        return BaseService.objects.create(
            instagram_information=instagramInformation, **validated_data
        )


class UGCServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)

    class Meta:
        model = UGCService
        exclude = ["instagram_information"]

    def create(self, validated_data):
        print("validated_data", validated_data)
        instagramInformation = InfluencerInstagramInformation.objects.get(
            instagram_id=validated_data["instagram_id"]
        )
        validated_data.pop("instagram_id")
        return UGCService.objects.create(
            instagram_information=instagramInformation, **validated_data
        )


class UGCServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGCService
        fields = "__all__"


class FeedPostServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)

    class Meta:
        model = FeedPostService
        exclude = ["instagram_information"]

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(
            instagram_id=validated_data["instagram_id"]
        )
        validated_data.pop("instagram_id")
        return FeedPostService.objects.create(
            instagram_information=instagramInformation, **validated_data
        )


class FeedPostServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedPostService
        fields = "__all__"


class StoryPostServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)

    class Meta:
        model = StoryPostService
        exclude = ["instagram_information"]

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(
            instagram_id=validated_data["instagram_id"]
        )
        validated_data.pop("instagram_id")
        return StoryPostService.objects.create(
            instagram_information=instagramInformation, **validated_data
        )


class StoryPostServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryPostService
        fields = "__all__"


class ReelPostServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)

    class Meta:
        model = ReelPostService
        exclude = ["instagram_information"]

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(
            instagram_id=validated_data["instagram_id"]
        )
        validated_data.pop("instagram_id")
        return ReelPostService.objects.create(
            instagram_information=instagramInformation, **validated_data
        )


class ReelPostServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelPostService
        fields = "__all__"


class OtherServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)

    class Meta:
        model = OtherService
        exclude = ["instagram_information"]

    def create(self, validated_data):
        instagramInformation = InfluencerInstagramInformation.objects.get(
            instagram_id=validated_data["instagram_id"]
        )
        validated_data.pop("instagram_id")
        return OtherService.objects.create(
            instagram_information=instagramInformation, **validated_data
        )


class OtherServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherService
        fields = "__all__"


class InstagramBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramBase
        fields = "__all__"


class InstagramInitialInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramInitialInformation
        fields = "__all__"


class InstagramDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramDetails
        fields = "__all__"


class InstagramGenderDemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramGenderDemographics
        fields = "__all__"


class InstagramAgeDemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAgeDemographics
        fields = "__all__"


class InstagramCityDemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramCityDemographics
        fields = "__all__"


class InstagramCountryDemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramCountryDemographics
        fields = "__all__"


class InstagramMediaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramMediaData
        fields = "__all__"


class InstagramMediaCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramMediaComment
        fields = "__all__"


class ContractCreateSerializer(serializers.ModelSerializer):
    influencer = serializers.CharField(write_only=True)
    business = serializers.CharField(write_only=True)
    isInfluencer = serializers.BooleanField(write_only=True)

    class Meta:
        model = Contract
        fields = ["influencer", "business", "isInfluencer"]

    def create(self, validated_data):
        isInfluencer = validated_data["isInfluencer"]
        validated_data.pop("isInfluencer")

        influencerUser = User.objects.get(username=validated_data["influencer"])
        influencerAccount = InfluencerAccount.objects.get(user=influencerUser)
        validated_data.pop("influencer")

        businessUser = User.objects.get(username=validated_data["business"])
        businessAccount = BusinessAccount.objects.get(user=businessUser)
        validated_data.pop("business")

        createdContract = Contract.objects.create(
            influencer=influencerAccount, business=businessAccount, **validated_data
        )
        if isInfluencer:
            ContractVersion.objects.create(
                contract=createdContract,
                contract_version=1,
                contract_text="",
                contract_date=timezone.now(),
                contract_visible=False,
                owner=influencerAccount.user,
                is_influencer=True,
            )
        else:
            ContractVersion.objects.create(
                contract=createdContract,
                contract_version=1,
                contract_text="",
                contract_date=timezone.now(),
                contract_visible=False,
                owner=businessAccount.user,
                is_influencer=False,
            )

        return createdContract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        business = BusinessAccount.objects.get(id=ret["business"])
        ret["business"] = business.user.username
        influencer = InfluencerAccount.objects.get(id=ret["influencer"])
        ret["influencer"] = influencer.user.username

        return ret


class ContractVersionCreateSerializer(serializers.ModelSerializer):
    contract_id = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    contract_version = serializers.IntegerField(read_only=True)

    class Meta:
        model = ContractVersion
        exclude = ["contract", "owner"]

    def create(self, validated_data):
        contract = Contract.objects.get(contract_id=validated_data["contract_id"])
        validated_data.pop("contract_id")
        user = User.objects.get(username=validated_data["username"])
        validated_data.pop("username")
        return ContractVersion.objects.create(
            contract=contract, owner=user, **validated_data
        )


class ContractVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractVersion
        fields = "__all__"


class ContractVersionTextUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractVersion
        exclude = ["contract", "contract_version", "owner"]

    def update(self, instance, validated_data):
        instance.contract_text = validated_data.get(
            "contract_text", instance.contract_text
        )
        instance.save()
        return instance


class SignatureRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureRequests
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        user = User.objects.get(id=ret["request_user"])
        ret["request_user"] = user.username

        contract = Contract.objects.get(contract_id=ret["contract"])
        instagramInitialInformation = InstagramInitialInformation.objects.get(
            influencer_instagram_information=contract.influencerInstagramInformation
        )
        ret["influencer"] = instagramInitialInformation.username

        ret["business"] = contract.business.company_name

        if ret["file"] != None:
            file = Files.objects.get(id=ret["file"])
            ret["file_name"] = file.file_name
            ret["file_size"] = file.file_size
            ret["file_date"] = file.file_date
        else:
            ret["file_name"] = None
            ret["file_size"] = None
            ret["file_date"] = None

        return ret


class SignatureRequestsCreateSerializer(serializers.ModelSerializer):
    # file_id = serializers.CharField(write_only=True)
    contract_id = serializers.CharField(write_only=True)
    version_id = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = SignatureRequests
        # fields = "__all__"
        exclude = ["contract", "contract_version", "request_user"]

    def create(self, validated_data):
        contract = Contract.objects.get(contract_id=validated_data["contract_id"])
        validated_data.pop("contract_id")
        version = ContractVersion.objects.get(
            contract=contract, contract_version=validated_data["version_id"]
        )
        validated_data.pop("version_id")
        user = User.objects.get(username=validated_data["username"])
        validated_data.pop("username")
        # file = Files.objects.get(id=validated_data["file_id"])
        # validated_data.pop("file_id")
        return SignatureRequests.objects.create(
            contract=contract,
            contract_version=version,
            request_user=user,
            # file=file,
            **validated_data
        )


class FileSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField()

    class Meta:
        model = Files
        fields = ["id", "file", "file_name", "file_date", "file_size", "selected"]

    def get_selected(self, obj):
        user = self.context.get("request_user")

        contract = self.context.get("contract")
        contract_version = self.context.get("contract_version")
        if user and contract and contract_version:
            # Get the latest signature request for the given contract, contract version, and user
            latest_request = (
                SignatureRequests.objects.filter(
                    request_user=user,
                    contract=contract,
                    contract_version=contract_version,
                    file=obj,
                )
                .order_by("-request_date")
                .first()
            )
            print(latest_request)
            if latest_request:
                return True
        return False


class UserFilesSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "files"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        contract = self.context.get("contract")
        contract_version = self.context.get("contract_version")
        request_user = instance  # The current user instance being serialized

        # Pass the context to each file serializer
        for file_data in representation["files"]:
            file_instance = instance.files.filter(id=file_data["id"]).first()
            file_serializer = FileSerializer(
                file_instance,
                context={
                    "request_user": request_user,
                    "contract": contract,
                    "contract_version": contract_version,
                },
            )
            file_data["selected"] = file_serializer.data["selected"]
        return representation


# class FileSerializer(serializers.ModelSerializer):
#     # selected = serializers.SerializerMethodField()

#     class Meta:
#         model = Files
#         fields = ["id", "file", "file_name", "file_date", "file_size"]


# class UserFilesSerializer(serializers.ModelSerializer):
#     files = FileSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ["id", "username", "files"]

#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     contract = self.context.get('contract')
#     #     contract_version = self.context.get('contract_version')
#     #     request_user = instance  # The current user instance being serialized

#     #     # Pass the context to each file serializer
#     #     for file_data in representation['files']:
#     #         file_instance = instance.files.filter(id=file_data['id']).first()
#     #         file_serializer = FileSerializer(
#     #             file_instance,
#     #             context={'request_user': request_user, 'contract': contract, 'contract_version': contract_version}
#     #         )
#     #         file_data['selected'] = file_serializer.data['selected']
#     #     return representation

class ServicePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePricing
        fields = ["pricing_type", "price"]

class ServiceSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    pricing = serializers.ListField(write_only=True)
    # pricing = ServicePricingSerializer(many=True, read_only=True, source="pricings")

    class Meta:
        model = Service
        # fields = "__all__"
        # exclude = ["influencer_instagram_information"]
        # include = ["pricing"]
        fields = ["instagram_id", "service_name", "service_type", "post_type", "post_length", "content_provider", "pricing", "id"]

    def create(self, validated_data):
        pricing_data = validated_data.pop("pricing")
        influencerInstagramInformation = InfluencerInstagramInformation.objects.get(
            instagram_id=validated_data["instagram_id"]
        )
        validated_data.pop("instagram_id")
        service = Service.objects.create(
            influencer_instagram_information=influencerInstagramInformation,
            **validated_data
        )
        for pricing in pricing_data:
            ServicePricing.objects.create(
                service=service,
                pricing_type=pricing["pricing_type"],
                price=pricing["price"],
            )

        return service
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        print(ret)
        ret["pricing"] = ServicePricingSerializer(instance.pricings.all(), many=True).data
        return ret
    
class RequestsSerializer(serializers.ModelSerializer):
    instagram_id = serializers.CharField(write_only=True)
    business_username = serializers.CharField(write_only=True)
    service_id = serializers.CharField(write_only=True)

    influencer = serializers.CharField(read_only=True)
    business = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)

    class Meta: 
        model = Requests
        exclude = []
    
    def create(self, validated_data):
        influencerInstagramInformation = InfluencerInstagramInformation.objects.get(instagram_id=validated_data["instagram_id"])
        validated_data.pop("instagram_id")
        user = User.objects.get(username=validated_data["business_username"])
        validated_data.pop("business_username")
        businessAccount = BusinessAccount.objects.get(user=user)

        service = Service.objects.get(id=validated_data["service_id"])
        validated_data.pop("service_id")
        return Requests.objects.create(business=businessAccount, influencer=influencerInstagramInformation.influencer, service=service, **validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["influencer"] = instance.influencer.id
        ret["business"] = instance.business.id
        ret["business_name"] = instance.business.company_name   
        ret["business_industry"] = instance.business.company_industry
        ret["business_location"] = instance.business.company_country
        ret["business_website"] = instance.business.company_website
        ret["business_username"] = instance.business.user.username
        ret["service"] = instance.service.id
        ret["service_name"] = instance.service.service_name
        servicePricing = instance.service.pricings.first()
        ret["service_price"] = servicePricing.price

        return ret
