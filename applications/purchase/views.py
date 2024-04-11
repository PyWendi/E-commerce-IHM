from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serialisers import PurchaseSerialiser, OrderSerialiser
from .models import Purchase, Order

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
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
