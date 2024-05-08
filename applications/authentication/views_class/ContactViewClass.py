from .commonImport import *
from ..serialisers import ContactSerialiser
from ..models import Notification, Contact

class ContactViewSet(viewsets.ModelViewSet):
    """
    Contact api which is used to pass command or sending a specific request
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerialiser
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete', 'update']]
    
    
    @swagger_auto_schema(request_body=ContactSerialiser, responses={
        200: "OK",
        400: "Erreur lors de l'envoi du contact.",
        500: "Une erreur est survenu, veuiller reessayer plutard."
    })
    def create(self, request, *args, **kwargs):
        try:
            data = {
                "name": request.data.get("name"),
                "email": request.data.get("email"),
                "text": request.data.get("text"),
            }
            Contact.objects.create(**data)
            
            admins = get_user_model().objects.filter(is_superuser=True).values_list("id")
            Notification.objects.bulk_create(
                [Notification(
                    owner_id=admin[0],
                    type="contact",
                ) for admin in admins]
            )
            
            trigger_channel("admin_notification", dict(type="admin_notification", operation=True))
            
            print("\nDone****")
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Erreur lors de l'insertion du contact",
                "Erreur": str(e)
            }, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
            
