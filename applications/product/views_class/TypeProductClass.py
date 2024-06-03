from .commonImport import *
from ..models import TypeProduct

from ..serialisers import (
    TypeProductSerializer,
    TypeAndProductSerialiser,
    TypeProductWithProductSerializer,
)


class TypeProductViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally, we also provide an extra `extend` action which return all product from a specific type
    """
    queryset = TypeProduct.objects.all()
    serializer_class = TypeProductSerializer
    authentication_classes = [JWTAuthentication]
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['patch']]

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return TypeProductWithProductSerializer
        return TypeProductSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        here, we only need specific permission for create and update method of the
        viewsets methods
        """
        if self.action in ["create", "update", "delete"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = []
        return super(TypeProductViewSet, self).get_permissions()


    @swagger_auto_schema(responses={200: TypeAndProductSerialiser(many=True), 400: "Not updated"})
    @action(methods=["GET"], detail=True)
    def all_products(self, request, pk=None):
        type = get_object_or_404(TypeProduct, pk=pk)
        serializer = TypeAndProductSerialiser(type)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(responses={200: TypeProductSerializer(many=True),404: "No category is matching the requested value"})
    @action(methods=["GET"], detail=False, url_path="search/(?P<value>[a-zA-Z]+)")
    def search_categories(self, request, value, *args, **kwargs):
        types = TypeProduct.objects.filter(designation__icontains=value)
        if types is None:
            return Response({"data": [],}, status=status.HTTP_404_NOT_FOUND)
        
        serialiser = self.serializer_class(types, many=True)
        return Response({"data": serialiser.data}, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(responses={200: TypeProductSerializer(many=True),404: "No category is matching the requested value"})
    @action(methods=["GET"], detail=False, url_path="order/(?P<value>[a-zA-Z]+)")
    def order_by(self, request, value, *args, **kwagrs):
        print(value)
        type = TypeProduct.objects.order_by("designation") if (value == "asc") else TypeProduct.objects.order_by("-designation")
        if type is None:
            return Response({"results": []}, status=status.HTTP_404_NOT_FOUND)
        serialiser = self.serializer_class(type, many=True)
        return Response({
            "results": serialiser.data
            }, status=status.HTTP_200_OK)
