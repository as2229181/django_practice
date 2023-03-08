"""
ASGI config for django_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see

"""
from channels.layers import get_channel_layer
from channels.routing import get_default_application
import django
import os
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddleware
import blog.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_demo.settings')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
        'websocket':AuthMiddleware( #當收到之後就必續導入authmiddleware裡面會call URLROUTER;authmiddleware可以知道人是誰)
        URLRouter(
            blog.routing.websocket_urlpatterns))
    }
)