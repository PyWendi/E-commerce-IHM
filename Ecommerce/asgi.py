"""
ASGI config for Ecommerce project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from applications.socket_extra_config.socket_custom_middleware import AllowAnyOriginMiddleware, AllowedOriginsMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application

import applications.authentication.socket_routing as auth_socket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')

django_asgi_app = get_asgi_application()

websocket_urlpatterns = []
websocket_urlpatterns.extend(auth_socket.websocket_urlpatterns)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedOriginsMiddleware(
            AuthMiddlewareStack(
                URLRouter(
                    websocket_urlpatterns
            )
        )
    )
})

#     URLRouter(
#     websocket_urlpatterns
# )
#     AllowedHostsOriginValidator(
#     # AuthMiddlewareStack(URLRouter(socket_routing.websocket_urlpatterns))
#     URLRouter(socket_routing.websocket_urlpatterns)
# )
