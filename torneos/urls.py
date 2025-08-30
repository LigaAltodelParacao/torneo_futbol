from django.urls import path, include
from rest_framework import routers
from .views import PartidoViewSet, EquipoViewSet, CategoriaViewSet, JugadorViewSet

router = routers.DefaultRouter()
router.register('partidos', PartidoViewSet)
router.register('equipos', EquipoViewSet)
router.register('categorias', CategoriaViewSet)
router.register('jugadores', JugadorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
