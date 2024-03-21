from rest_framework import viewsets
from .serialisers import PurchaseSerialiser
from .models import Purchase


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    This API provide most action for performing CRUD operation on the `TypeProduct` model
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerialiser
