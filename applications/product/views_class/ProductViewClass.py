from .commonImport import *
from ..models import Product, Rating, TypeProduct
from ..serialisers import (
    ProductSerializer,
    ProductImageUpdateSerialiser,
    RateSerialiser,
    TypeAndProductSerialiser
)

class ProductViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally, we also provide an extra `extend` action which return all product from a specific type
    """
    queryset = Product.objects.order_by("-name")
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete']]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        here, we only need specific permission for create and update method of the
        viewsets methods
        """
        if self.action in ["create", "update", "delete", "update_image"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = []
        return super(ProductViewSet, self).get_permissions()

    def perform_create(self, serializer):
        type_id = self.request.data.get("type")
        type_product = TypeProduct.objects.get(pk=type_id)
        serializer.save(type=type_product)

    """-------Extra views--------"""

    @action(
        methods=["PUT"],
        detail=True,
        parser_classes=[MultiPartParser, FormParser],
        serializer_class=ProductImageUpdateSerialiser,
    )
    async def update_image(self, request, pk):
        """
        Add an extra method which alow to update the image of a specific product
        @param request:
        @param pk:
        @return file url:
        """
        product = await get_object_or_404(Product, pk=pk)
        image = request.FILES.get("image") if request.FILES.get("image") else None
        data = {"image": image}
        serializer = self.serializer_class(product, data=data)

        if serializer.is_valid():
            await serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(methods=["POST"] ,request_body=RateSerialiser, responses={201: "{'rate': rate_value}", 400: "Not updated"})
    @action(
        methods=["POST"],
        detail=True,
        serializer_class=RateSerialiser,
    )
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
    
    
    @swagger_auto_schema(methods=["GET"] , responses={201: "{'rate': rate_value}", 400: "Not updated"})
    @action(
        methods=["GET"],
        detail=False,
        url_path="search/name/(?P<search>[a-zA-Z]+)"
    )
    def lookup(self, request, search=None):
        """
        _summary_
        ```
        #This API is used to search products by their name which is inserted in the url
        @request -> str:[a-zA-Z]+
        ```
        """
        try:
            if not search.isalpha():
                return Response({
                    "Error": "La recherche doit seulement contenir des carateres alphabetiques."
                }, status=status.HTTP_400_BAD_REQUEST)
            products = Product.objects.filter(name__icontains=search)
            serializer = self.serializer_class(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "Message": "Une erreur s'est produite, veuiller reesayer plutard.",
                "Error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(methods=["GET"], responses={200: TypeAndProductSerialiser(many=True), 400: "Problem while fecthing the data"})
    @action(
        methods=["GET"],
        detail=True,
        serializer_class=TypeAndProductSerialiser,
    )
    def by_category(self, request, pk=None):
        type = TypeProduct.objects.order_by("designation")[:1] if not pk.isalpha() else get_object_or_404(TypeProduct, pk=pk)
        print(type)
        serialiser = TypeAndProductSerialiser(type, many=True)
        return Response(serialiser.data, status=status.HTTP_200_OK)

