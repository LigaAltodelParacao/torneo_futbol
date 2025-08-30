import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import torneos.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torneo_futbol.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(torneos.routing.websocket_urlpatterns),
})
