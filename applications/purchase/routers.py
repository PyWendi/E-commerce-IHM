from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet

router = DefaultRouter()

# Route register
router.register(r"purchase", PurchaseViewSet, basename="purchase")