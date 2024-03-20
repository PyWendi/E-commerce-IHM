from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

# Permissions and authentication system
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serialisers import TypeProductSerializer, ProductSerializer, TypeAndProductSerialiser, ProductImageUpdateSerialiser, RateSerialiser
from .models import TypeProduct, Product, Rating


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

    @action(methods=["PUT"], detail=True, parser_classes=[MultiPartParser, FormParser], serializer_class=ProductImageUpdateSerialiser)
    def update_image(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        image = request.FILES.get("image") if request.FILES.get("image") else None
        data = {"image": image}
        serializer = self.serializer_class(product, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=RateSerialiser, responses={201: "{'rate': rate_value}", 400: "Not updated"})
    @action(methods=["POST"], detail=True, serializer_class=RateSerialiser)
    def rate(self, request, pk):
        """
        ```
        $ '[Set rating for a product]'
        Need the following data to work properly:
        ```
        ```
        {
            token: 'placed in the Authorization (In the request header)',
            product_id: 'in the url',
            rate_value: 'The value of the rate done by the user'
        }
        ```
        `RETURN THE AVERAGE FINALE RATE VALUE`
        """
        product = get_object_or_404(Product, pk=pk)
        rate_value = int(request.data["rate_value"] if request.data["rate_value"] else 0)
        Rating.objects.update_or_create(
            product=product.id,
            user_id=request.user.id,
            defaults={"product": product, "user_id": request.user.id, "rate_value": rate_value}
        )

        # We take the average value of rating for a product
        rate = Rating.objects.filter(product=product).aggregate(average_rate=Avg("rate_value"))
        product.rate = int(rate["average_rate"])
        product.save()
        return Response({"rate": product.rate}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        type_id = self.request.data.get("type")
        type_product = TypeProduct.objects.get(pk=type_id)
        serializer.save(type=type_product)
