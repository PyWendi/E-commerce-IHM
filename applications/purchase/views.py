from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

# Handle third party's
# from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from decimal import Decimal

# Handle permission and authentication for the views
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

# Handle model
from django.contrib.auth import get_user_model
from .models import Purchase, Order
# from django.db.models import F
from applications.authentication.models import Notification
from .serialisers import PurchaseSerialiser, PurchaseWithDetailedSerialiser, OrderSerialiser, PurchaseForUpdateSerialiser
from applications.authentication.serialisers import NotificationSeriliser
from applications.product.models import Product

# Handle channel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



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
        if self.action == 'retrieve':
            return PurchaseWithDetailedSerialiser
        return PurchaseSerialiser
        # elif self.action == "create":
        #     return PurchaseOperationSerialiser

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
        client = self.request.user
        serializer.save(client=client)


    def trigger_channel(self, room, data):
        channel = get_channel_layer()
        async_to_sync(channel.group_send)(room, data)


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
            mont    ant: <montant>
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
            return Response(
                {
                    "Erreur": "Veuiller verifier les informations inserer",
                    "type": e
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        methods=["PUT"],
        request_body=PurchaseSerialiser,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["PUT"], detail=True, serializer_class=PurchaseForUpdateSerialiser)  # purchse/:pk/delivery
    def delivery(self, request, pk):
        """
        Need the following schema to run properly
        ```
        @request body = {
           client: <clientId>(int),
           delivery_date: <delivery_date>(date|string)
        }
        ```
        Via socket return 1
        """
        purchase = get_object_or_404(Purchase, pk=pk)
        serialiser = self.serializer_class(purchase, data={
            "is_delivered": True,
            "delivery_date": request.data.get("delivery_date")
        })
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        user = get_user_model().objects.get(pk=serialiser.data["client"])

        # Create notification to the user
        data = {
            "owner": serialiser.data["client"],
            "sender": request.user.id,
            "type": "livraison",
            "purchaseId": serialiser.data["id"]
        }

        notifSerialiser = NotificationSeriliser(data=data, many=False)
        notifSerialiser.is_valid(raise_exception=True)
        notifSerialiser.save()

        try:
            self.trigger_channel(
                f"client_{user.id}_notification",
                {
                    "type": "client_notification",
                    "operation": True
                })

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Une erreur est survenu, veuiller reessayer plutard.",
                "Erreur": e
            })


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

    # @sync_to_async()
    def trigger_channel(self, room, message_data):
        channel = get_channel_layer()
        async_to_sync(channel.group_send)(room, message_data)

    # This fonction us used to handle multiple insertion of an instance
    def mass_notification_assignement(self, request):
        try:
            serialiser = self.serializer_class(data=request.data.get("orders"), many=True)
            # orders = serialiser.validated_data
            # Order.objects.bulk_create([Order(**order) for order in orders])

            if serialiser.is_valid():
                serialiser.save()

                # Substract stock from data in the orders
                for order in request.data.get("orders"):
                    product = Product.objects.get(pk=order["product"])
                    product.stock -= order["quantity"]
                    product.save()

                return True
            return Response(data={
                "message": "Erreur lors de la creation des commandes",
                "error": serialiser.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={
                "message": "Une erreur est servenu, veuiller reessayer.",
                "erreur": e
            })

    # @database_sync_to_async
    @swagger_auto_schema(request_body=OrderSerialiser, responses={
        200: "OK",
        400: "Erreur lors de la validation de l'achat.",
        500: "Une erreur est survenu, veuiller reessayer plutard."
    })
    def create(self, request, *args, **kwargs):
        """
        The create methode request the following data:
        ```
            @body request = {
                purchaseId: <purchaseId>(int),
                indexes: <[index]>(array of index)(integer),
                orders: [{
                    purchase: purchaseID(int),
                    product: productId(int),
                    quantity: quantite(int)
                }]
            }
        ```
        ```@return status=200:```
        """
        if isinstance(request.data.get("orders"), list):
            order_creation_done = self.mass_notification_assignement(request)

            if order_creation_done:
                # Creating notification from user to admin
                admins = get_user_model().objects.filter(is_superuser=True).values_list("id")
                try:

                    Notification.objects.bulk_create(
                        [Notification(
                            owner_id=admin[0],
                            sender=request.user.id,
                            type="achat",
                            purchaseId=int(request.data.get("purchaseId"))
                        ) for admin in admins]
                    )

                except Exception as e:
                    return Response({
                        "Erreur": e,
                        "message": "Une erreur est survenu, veuiller reessayer plutard."
                    }, status=status.HTTP_400_BAD_REQUEST)


                data_to_be_rerendered_to_frontend = {
                    "indexes": request.data.get("indexes") if (isinstance(request.data.get("indexes"), list)) else [],
                    "orders": request.data.get("orders")
                }
                """
                This one is used to trigger the refetch of the latest admin notification
                """
                self.trigger_channel(
                    "admin_notification",
                    dict(type="admin_notification", operation=True)
                )
                """
                This one is used to send the inserted data to all user so client side can
                can re-ajust the stock for each product that has been ordered here
                """
                self.trigger_channel(
                    "client_rerend",
                    dict(type="client_rerend",data=data_to_be_rerendered_to_frontend)
                )

                return Response(data=dict(message="Paement effectuer avec succes."), status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Veuiller envoyer une liste des commandes conformes au norme de la requete"
        }, status=status.HTTP_400_BAD_REQUEST)

