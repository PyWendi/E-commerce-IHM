from rest_framework.routers import DefaultRouter
from . import views as v

router = DefaultRouter()

router.register(r"type_product", v.TypeProductViewSet, basename="typeproduct")
router.register(r"product", v.ProductViewSet, basename="product")
