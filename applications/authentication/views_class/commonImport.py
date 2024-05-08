from django.contrib.auth import get_user_model
from django.http import Http404
# from django.http import FileResponse
# from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

# handle rest views
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# handle token behavior
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

# Handle swagger
from drf_yasg.utils import swagger_auto_schema

# Handle channel
from applications.utilities.channel_method import trigger_channel
