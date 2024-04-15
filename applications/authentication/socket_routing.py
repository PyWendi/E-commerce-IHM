from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"notification/client/(?P<clientId>\w+)/$", consumers.ClientConsummer.as_asgi()),
    re_path(r"interaction/client/rerend/$", consumers.ClientRerendInterfaceConsumer.as_asgi()),
    re_path(r"notification/admin/$", consumers.AdminNotificationConsummer.as_asgi()),
]
