from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack

class AllowAnyOriginMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope["headers"] =[
            (b'host', b'localhost:8000'),
            (b'connection', b'upgrade'),
            (b'upgrade', b'websocket'),
            (b'sec-websocket-key', b'...'),
            (b'sec-websocket-version', b'13'),
        ]

        return await super().__call__(scope, receive, send)

class AllowedOriginsMiddleware(BaseMiddleware):
    allowed_origins = [
        "http://127.0.0.1",
        # "https://example.com",
    ]

    async def __call__(self, scope, receive, send):
        if "origin" in scope.get("headers", []):
            origin = scope["headers"][scope["headers"].index(b'origin') + 1].decode()
            if origin not in self.allowed_origins:
                raise ValueError("Origin not allowed !")

        return await super().__call__(scope, receive, send)
