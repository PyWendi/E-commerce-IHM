from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NotificationViewset

router = DefaultRouter()
router.register(r"client", UserViewSet, basename="customuser")
router.register(r"notification", NotificationViewset, basename="notification")