from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.db.models import Avg, QuerySet
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

# Permissions and authentication system
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
