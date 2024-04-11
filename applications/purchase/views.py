from rest_framework import viewsets
from .serialisers import PurchaseSerialiser, OrderSerialiser
from .models import Purchase, Order

from django.db.models import QuerySet

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
        if self.action in ["create", "update", "update_image", "rate"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(PurchaseViewSet, self).get_permissions()
IsAuthenticated

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
