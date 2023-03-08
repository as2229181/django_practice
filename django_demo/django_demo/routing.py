from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter,URLRouter
import blog.routing
import os
from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer


# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
# })

channel_layer = get_channel_layer()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    'websocket':AuthMiddleware( #當收到之後就必續導入authmiddleware裡面會call URLROUTER;authmiddleware可以知道人是誰)
        URLRouter(
            blog.routing.websocket_urlpatterns))
})