from .commonImport import *
from ..models import Purchase
from ..serialisers import (
    PurchaseSerialiser,
    PurchaseWithDetailedSerialiser,
    PurchaseForUpdateSerialiser
)
from applications.authentication.serialisers import NotificationSeriliser
from applications.utilities.channel_method import trigger_channel
from rest_framework.pagination import PageNumberPagination

class PurchasePagination(PageNumberPagination):
    page_size = 5

class PurchaseViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    To create a `Purchase`, you just need to provide the `token from authentication`

    ```
    Perform `create`, `list`, `read` operations

    For the creation just provide the following data and
    not the body request showcase in the request sample

    @body = {
        address: <adress>(string),
        payement_mode: <payement_mode>(string),
        account_number: <account_number>(string)
    }
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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        here, we only need specific permission for create and update method of the
        viewsets methods
        """
        if self.action in ["update", "update_image"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            # self.permission_classes = [IsAuthenticated]
            pass
        return super(PurchaseViewSet, self).get_permissions()

    def perform_create(self, serializer):
        client = self.request.user
        serializer.save(client=client)

    @swagger_auto_schema(
        method="GET",
        responses=({
            200: "OK, List of purchase", 400: "Erreur innatendue", 500: "Erreur innatendu du serveur"
        }),
        # operation_summary="Les donnees envoyer dans le corps de la request (purchaseId) est utiliser pour creed des notification qui seront envoyer vers les administrateurs"
    )
    @action(methods=["GET"], detail=False, url_path="for/user")
    def for_a_user(self, request, page=None, *args, **kwargs):
        """
        Retrieves all purchases for the authenticated user, paginated.
        This endpoint is intended for use in the user profile section.

        @param request: The incoming HTTP request object.
        @return: A paginated response containing serialized purchase data.
        """
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        purchase = user.purchase_set.all()

        paginator = PurchasePagination()  # Create a paginator instance
        paginated_purchase = paginator.paginate_queryset(purchase, request)  # Apply pagination

        serializer = self.serializer_class(paginated_purchase, many=True)
        response_data = {"results": serializer.data}

        # Include pagination information in the response (optional)
        if paginated_purchase is not None:
            response_data['count'] = paginator.page.paginator.count  # Total number of purchases
            if paginator.page.has_previous():
                response_data['previous'] = paginator.get_previous_link()
            if paginator.page.has_next():
                response_data['next'] = paginator.get_next_link()

        return Response(response_data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        methods=["PUT"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(
        methods=["PUT"],
        detail=False,
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
        Dans le cas ou le montant est superieur au solde, on obtient le status code ```400``` et le data ```{"message": "Montant superieur au solde du client"}``` en tant
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
                    "type": str(e)
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
            trigger_channel(
                f"client_{user.id}_notification",
                {
                    "type": "client_notification",
                    "operation": True
                })

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Une erreur est survenu, veuiller reessayer plutard.",
                "Erreur": str(e)
            })
