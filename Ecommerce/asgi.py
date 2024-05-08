import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application

from applications.utilities.socket_extra_config.socket_custom_middleware import AllowedOriginsMiddleware
import applications.utilities.socket.socket_routing as auth_socket

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
