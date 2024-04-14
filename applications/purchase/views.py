from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serialisers import PurchaseSerialiser , PurchaseWithDetailedSerialiser, OrderSerialiser
from drf_yasg.utils import swagger_auto_schema

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from .models import Purchase, Order
from applications.product.models import Product
from django.shortcuts import get_object_or_404
from decimal import Decimal

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    To create a `Purchase`, you just need to provide the `token from authentication`

    ```
    Perform `create`, `list`, `read` operations
    ```
    """
    serializer_class = PurchaseSerialiser
    queryset = Purchase.objects.all()
    authentication_classes = [JWTAuthentication]
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete', 'patch']]

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['retrieve']:
            return PurchaseWithDetailedSerialiser
        return PurchaseSerialiser

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        here, we only need specific permission for create and update method of the
        viewsets methods
        """
        if self.action in ["update", "update_image"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(PurchaseViewSet, self).get_permissions()

    def perform_create(self, serializer):
        adress = self.request.POST.get("adress")
        client = self.request.user
        serializer.save(client=client)



    @action(
        methods=["PUT"],
        detail=False,
        serializer_class=[PurchaseSerialiser]
    )
    def validate_payement(self, request):
        """
        Valider le payement de l'utilisateur, Attend les information suivante
        ```
        {
            montant: <montant>
        }
        ```
        Retourne le status_code ```200``` et le data ```{"message": "Transaction effectue."}``` en tant que reponse.
        Dans le cas ou le montant est superieur au solde, on obtient le status code ```200``` et le data ```{"message": "Montant superieur au solde du client"}``` en tant
        que reponse.
        """
        user = get_user_model()
        user = user.objects.get(pk=request.user.id)
        try:
            montant = Decimal(str(request.data.get("montant")))
            if montant > user.solde:
                return Response(
                    {"message": "Montant superieur au solde du client"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.solde -= montant
            user.save()
            return Response(
                {"message": "Transaction effectue."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {"Erreur": "Veuiller verifier les informations inserer"},
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderViewSets(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.```
    Perform `create`, `list`, `read` operations
    ```

    ```
    Perform `create`, `list`, `read` operations
    ```

    The create methode request the following data:
    ```@param request, [{
    purchase: purchaseID(int),
    product: productId(int),
    quantite: quantite(int)```
    """
    serializer_class = OrderSerialiser
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete', 'patch']]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        here, we only need specific permission for create and update method of the
        viewsets methods
        """
        if self.action in ["update", "delete"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(OrderViewSets, self).get_permissions()

    # This function us used to handle multiple insertion of an instance
    def bulk_create(self, request):
        try:
            serialiser = self.serializer_class(data=request.data, many=True)
            if serialiser.is_valid(raise_exception=True):
                data = serialiser.save()
                return Response(status=status.HTTP_201_CREATED)
                # orders = serialiser.validated_data
                # Order.objects.bulk_create([Order(**order) for order in orders])
            return Response(data={
                "message": "Erreur lors de la creation des commandes",
                "error": serialiser.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={
                "message": "Une erreur est servenu, veuiller reessayer.",
                "erreur": e
            })


    @swagger_auto_schema(request_body=OrderSerialiser ,responses={200: "OK", 400: "Erreur lors de la validation de l'achat.", 500: "Une erreur est survenu, veuiller reessayer plutard."})
    def create(self, request, *args, **kwargs):
        """
        The create methode request the following data:
        ```
            @body request = [{
                purchase: purchaseID(int),
                product: productId(int),
                quantity: quantite(int)
            }]

        ```
        ```@return status=200:```
        """
        if isinstance(request.data, list):
            return self.bulk_create(request)
        return Response({
            "message": "Veuiller envoyer une liste des commandes conformes au norme de la requete"
        }, status=status.HTTP_400_BAD_REQUEST)
