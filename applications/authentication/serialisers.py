from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UploadedFile, Notification, Contact
from applications.purchase.serialisers import Purchase, PurchaseSimpleDataSerialiser

from applications.purchase.serialisers import PurchaseForUserSerialiser

"""
Custom the content of the token generated
"""


class CustomTokenObtainPairSerialiser(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["isAdmin"] = user.is_superuser
        return token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    # snippets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # snippets = SnippetSerializer(many=True)

    profile_img = serializers.ImageField(read_only=True)
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(write_only=True)
    is_staff = serializers.BooleanField(write_only=True)
    is_superuser = serializers.BooleanField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'url',
            'id',
            'first_name',
            "last_name",
            "email",
            "password",
            "profile_img",
            "is_active",
            "is_staff",
            "is_superuser",
            "birthdate",
            "card_number",
            "solde",
        ]

    def create(self, validated_data):
        user = get_user_model()
        return user.objects.create_user(**validated_data)
    
    
    
class UserPurchaseSerializer(serializers.ModelSerializer):
    
    purchases = PurchaseForUserSerialiser(source="purchase_set", many=True)
    
    class Meta:
        model = get_user_model()
        fields = ["id", "purchases"]






class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["profile_img"]


class NotificationSeriliser(serializers.ModelSerializer):
    purchase_details = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    expiration_duration = serializers.DurationField(read_only=True)
    seen = serializers.BooleanField(required=False)

    class Meta:
        model = Notification
        fields = "__all__"

    def get_purchase_details(self, obj):
        purchaseId = obj.purchaseId
        try:
            purchase = Purchase.objects.get(pk=purchaseId)
            serialiser = PurchaseSimpleDataSerialiser(purchase)
            return serialiser.data
        except Purchase.DoesNotExist:
            print("No purchase found on get extra content.")
            return None


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file',)


"""
Contact serialiser
"""
class ContactSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
