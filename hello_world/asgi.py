"""
ASGI config for hello_world project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import re_path

from app.simple_app.consumers import EchoConsumer, BingoConsumer, BMIConsumer
from app.social_network.consumers import SocialNetworkConsumer
from app.route_map.consumer import MapConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    # Websocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^ws/echo/$", EchoConsumer.as_asgi()),
            re_path(r"^ws/bingo/$", BingoConsumer.as_asgi()),
            re_path(r"^ws/bmi/$", BMIConsumer.as_asgi()),
            re_path(r"^ws/social-network/$", SocialNetworkConsumer.as_asgi()),
            re_path(r"^ws/route-map/$", MapConsumer.as_asgi()),
        ])
    )
})




