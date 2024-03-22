from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet, OrderViewSets

router = DefaultRouter()

# Route register
router.register(r"purchase", PurchaseViewSet, basename="purchase")
router.register(r"order", OrderViewSets, basename="order")