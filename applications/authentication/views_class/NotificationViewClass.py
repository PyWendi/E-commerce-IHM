from .commonImport import *
from ..serialisers import NotificationSeriliser
from ..models import Notification

class NotificationViewset(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `NOTIFICATION` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally, we also provide an extra `send_notif_to_admin` action.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSeriliser
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete']]

    # Get all notification for a user
    @swagger_auto_schema(
        method="GET",
        responses=({
            200: "OK", 400: "Erreur innatendue", 500: "Erreur innatendu du serveur"
        }),
        # operation_summary="Les donnees envoyer dans le corps de la request (purchaseId) est utiliser pour creed des notification qui seront envoyer vers les administrateurs"
    )
    @action(methods=["GET"], detail=False, url_path="for/user")
    def for_a_user(self, request):
        """
        Return all `notification for a user`, admin or not
        """
        notification = Notification.objects.filter(owner=request.user.id)
        serialiser = NotificationSeriliser(notification, many=True)
        return Response(serialiser.data, status=status.HTTP_200_OK)
        

    @swagger_auto_schema(
        method="PUT",
        responses=({
            200: "OK", 404: "Users Admin not found", 500: "Erreur innatendu du server"
        }),
        # operation_summary="Les donnees envoyer dans le corps de la request (purchaseId) est utiliser pour creed des notification qui seront envoyer vers les administrateurs"
    )
    @action(methods=["PUT"], detail=True)
    def marked_as_seen(self, request, pk):
        """
        Need only the `notificatonId` to operate and return a `status 200`
        """
        notification = get_object_or_404(Notification, pk=pk)
        notification.seen = True
        notification.save()

        return Response(status=status.HTTP_200_OK)
    
