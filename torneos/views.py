from rest_framework import viewsets
from .models import Partido, Equipo, Categoria, Jugador
from .serializers import PartidoSerializer, EquipoSerializer, CategoriaSerializer, JugadorSerializer

# ViewSet para los partidos
class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer

# ViewSet para equipos
class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

# ViewSet para categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# ViewSet para jugadores
class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer