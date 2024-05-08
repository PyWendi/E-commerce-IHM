from .commonImport import *
from ..models import Order
from applications.authentication.models import Notification
from applications.product.models import Product
from ..serialisers import OrderSerialiser
from applications.utilities.channel_method import trigger_channel


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


    # This fonction us used to handle multiple insertion of an instance
    def mass_orders_update(self, request):
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
                "erreur": str(e)
            })

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
                    purchase: <purchaseID>(int),
                    product: <productId>(int),
                    quantity: <quantite>(int)
                }]
            }
        ```
        `@return status=200:`
        All methode also trigger two `channels` which handle `client` `interface re-render`
        | `client_rerend` and `admin_notification`
        """
        if isinstance(request.data.get("orders"), list):
            order_creation_done = self.mass_orders_update(request)

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
                        "Erreur": str(e),
                        "message": "Une erreur est survenu, veuiller reessayer plutard."
                    }, status=status.HTTP_400_BAD_REQUEST)


                data_to_be_rerendered_to_frontend = {
                    "indexes": request.data.get("indexes") if (isinstance(request.data.get("indexes"), list)) else [],
                    "orders": request.data.get("orders")
                }
                """
                This one is used to trigger the refetch of the latest admin notification
                """
                trigger_channel(
                    "admin_notification",
                    dict(type="admin_notification", operation=True)
                )
                """
                This one is used to send the inserted data to all user so client side can
                can re-ajust the stock for each product that has been ordered here
                """
                trigger_channel(
                    "client_rerend",
                    dict(type="client_rerend",data=data_to_be_rerendered_to_frontend)
                )

                return Response(data=dict(message="Paement effectuer avec succes."), status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Veuiller envoyer une liste des commandes conformes au norme de la requete"
        }, status=status.HTTP_400_BAD_REQUEST)

