from .commonImport import *

# Handle serialiser and models
from ..serialisers import ProfileImageSerializer




class ProfileSetView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=ProfileImageSerializer, responses={201: "CREATED", 400: "Not updated"})
    def post(self, request, *args, **kwargs):
        serializer = ProfileImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProfileImageSerializer, responses={200: "Updated", 400: "Not updated"})
    def put(self, request, pk, *args, **kwargs):
        user = get_user_model().objects.get(pk=pk)
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}
        serializer = ProfileImageSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


