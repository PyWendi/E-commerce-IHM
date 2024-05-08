from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, NotificationViewset, ContactViewSet

from .views_class.CustomuserViewClass import UserViewSet
from .views_class.NotificationViewClass import NotificationViewset
from .views_class.ContactViewClass import ContactViewSet

router = DefaultRouter()
router.register(r"client", UserViewSet, basename="customuser")
router.register(r"notification", NotificationViewset, basename="notification")
router.register(r"contact", ContactViewSet, basename="contact")