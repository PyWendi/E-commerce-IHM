from .commonImport import *

from ..serialisers import CustomTokenObtainPairSerialiser

from ..serialisers import (
    ProfileImageSerializer, 
    UserSerializer, 
    UserPurchaseSerializer,
    )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Customise the token which will return within the api
    """
    serializer_class = CustomTokenObtainPairSerialiser
    


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


    @swagger_auto_schema(
        methods=["PUT"],
        request_body=ProfileImageSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=True, parser_classes=[MultiPartParser, FormParser], serializer_class=ProfileImageSerializer)
    async def update_profile(self, request, pk):
        # user = await get_object_or_404(get_user_model(), pk=pk)
        user = request.user
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}

        serializer = self.serializer_class(user, data=data)
        if serializer.is_valid():
            await serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(
        methods=["GET"],
        responses={
            200: "OK", 
            400: "BAD request", 
            500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False, serializer_class=UserPurchaseSerializer)
    def purchase_list(self, request):
        user = request.user
        try:
            serialiser = UserPurchaseSerializer(user)
            return Response(serialiser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "Error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
