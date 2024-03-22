from django.contrib.auth import get_user_model
from django.http import Http404
from django.http import FileResponse
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

# handle rest views
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, action

# handle token behavior
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serialisers import CustomTokenObtainPairSerialiser

# Handle swagger
from drf_yasg.utils import swagger_auto_schema

from .serialisers import ProfileImageSerializer, FileUploadSerializer, UserSerializer
from .models import UploadedFile


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Customise the token which will return within the api
    """
    serializer_class = CustomTokenObtainPairSerialiser
    # def get_token_for_user(self,user):
    #     pass

class UserViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `client` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally, we also provide an extra `update_profile` action.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete']]

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()

    def get_authenticators(self):
        """
        Instantiates and returns the list of authentication classes that this view requires.
        """
        request_method = self.request.method.lower()
        if request_method == 'post':
            return []
        else:
            return [JWTAuthentication()]
        return super(UserViewSet, self).get_authenticators()

    @action(methods=["put"], detail=True, parser_classes=[MultiPartParser, FormParser], serializer_class=ProfileImageSerializer)
    async def update_profile(self, request, pk):
        user = await get_object_or_404(get_user_model(), pk=pk)
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}

        serializer = self.serializer_class(user, data=data)
        if serializer.is_valid():
            await serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(request_body=FileUploadSerializer, responses={200: "Updated", 400: "Not updated"})
class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    async def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            await serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
async def download_file(request, pk):
    # Retrieve the UploadedFile instance by its primary key (pk)
    # uploaded_file = get_object_or_404(UploadedFile, pk=pk)
    user = await get_object_or_404(get_user_model(), pk=pk)
    # Use FileResponse to serve the file
    # The as_attachment=True parameter prompts the browser to download the file
    # return FileResponse(uploaded_file.file.open(), as_attachment=True)
    return Response({
        "file_link": user.profile_img.url
    })

def get_object(pk):
    user = get_user_model()
    try:
        return user.objects.get(pk=pk)
    except user.DoesNotExist:
        raise Http404


class ProfileUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ProfileImageSerializer, responses={200: "Updated", 400: "Not updated"})
    async def put(self, request, pk, *args, **kwargs):
        user = await get_user_model().objects.get(pk=pk)
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}
        serializer = ProfileImageSerializer(user, data=data)
        if serializer.is_valid():
            await serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "OK"})
    async def get(self, request, pk, format=None):
        user = await get_object(pk)
        serializer = ProfileImageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileSetView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ProfileImageSerializer, responses={201: "CREATED", 400: "Not updated"})
    async def post(self, request, *args, **kwargs):
        serializer = ProfileImageSerializer(data=request.data)
        if serializer.is_valid():
            await serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)