from django.urls import re_path, path
from . import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from accounts import consumers as accounts_consumers
websocket_urlpatterns = [
    re_path(r"ws/chat/lobby/$", consumers.TestConsumer.as_asgi()),
    #path("trading/equity/", accounts_consumers.EquityConsumer.as_asgi()),

]
