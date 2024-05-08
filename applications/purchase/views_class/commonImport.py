from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

# Handle third party's
# from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from decimal import Decimal

# Handle permission and authentication for the views
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


# Custom user model
from django.contrib.auth import get_user_model