from django.contrib.auth import get_user_model
from django.http import Http404
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, action

from drf_yasg.utils import swagger_auto_schema

from .serialisers import ProfileImageSerializer, FileUploadSerializer, UserSerializer
from .models import UploadedFile


class UserViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the client model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally, we also provide an extra `update_profile` action.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @action(methods=["put"], detail=True, parser_classes=[MultiPartParser, FormParser], serializer_class=ProfileImageSerializer)
    def update_profile(self, request, pk):
        # print(request.FILES)
        user = get_object_or_404(get_user_model(), pk=pk)
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}

        serializer = self.serializer_class(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(request_body=FileUploadSerializer, responses={200: "Updated", 400: "Not updated"})
class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def download_file(request, pk):
    # Retrieve the UploadedFile instance by its primary key (pk)
    # uploaded_file = get_object_or_404(UploadedFile, pk=pk)
    user = get_object_or_404(get_user_model(), pk=pk)
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
    def put(self, request, pk, *args, **kwargs):
        print(request.FILES)
        user = get_user_model().objects.get(pk=pk)
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}
        serializer = ProfileImageSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "OK"})
    def get(self, request, pk, format=None):
        user = get_object(pk)
        serializer = ProfileImageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileSetView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ProfileImageSerializer, responses={201: "CREATED", 400: "Not updated"})
    def post(self, request, *args, **kwargs):
        serializer = ProfileImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)