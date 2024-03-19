from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

# Permissions and authentication system
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serialisers import TypeProductSerializer, ProductSerializer, TypeAndProductSerialiser
from .models import TypeProduct, Product


class TypeProductViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally, we also provide an extra `extend` action which return all product from a specific type
    """
    queryset = TypeProduct.objects.all()
    serializer_class = TypeProductSerializer

    @swagger_auto_schema(responses={200: TypeAndProductSerialiser(many=True), 400: "Not updated"})
    @action(methods=["GET"], detail=True)
    def all_products(self, request, pk=None):
        type = get_object_or_404(TypeProduct, pk=pk)
        serializer = TypeAndProductSerialiser(type)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally, we also provide an extra `extend` action which return all product from a specific type
    """
    queryset = Product.objects.order_by("-name")
    serializer_class = ProductSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        type_id = self.request.data.get("type")
        type_product = TypeProduct.objects.get(pk=type_id)
        serializer.save(type=type_product)

