from django.urls import re_path

from .consumers.AdminNotificationConsumerClass import AdminNotificationConsummer
from .consumers.ClientConsumerClass import ClientConsummer
from .consumers.ClientRerendInterfaceConsumerClass import ClientRerendInterfaceConsumer

websocket_urlpatterns = [
    re_path(r"notification/client/(?P<clientId>\w+)/$", ClientConsummer.as_asgi()),
    re_path(r"interaction/client/rerend/$", ClientRerendInterfaceConsumer.as_asgi()),
    re_path(r"notification/admin/$", AdminNotificationConsummer.as_asgi()),
]
