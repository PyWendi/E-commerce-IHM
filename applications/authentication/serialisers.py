from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UploadedFile

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
    is_staff = serializers.BooleanField(write_only=True)
    is_superuser = serializers.BooleanField()

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
            "is_staff",
            "is_superuser",
            "birthdate",
            "card_number",
            "solde",
            # 'snippets'
        ]


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["profile_img"]


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file',)
