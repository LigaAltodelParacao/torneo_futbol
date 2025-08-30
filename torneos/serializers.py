from rest_framework import serializers
from .models import Categoria, Equipo, Jugador, Cancha, Partido, EventoPartido

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: model = Categoria; fields = "__all__"

class EquipoSerializer(serializers.ModelSerializer):
    class Meta: model = Equipo; fields = "__all__"

class JugadorSerializer(serializers.ModelSerializer):
    class Meta: model = Jugador; fields = "__all__"

class CanchaSerializer(serializers.ModelSerializer):
    class Meta: model = Cancha; fields = "__all__"

class PartidoSerializer(serializers.ModelSerializer):
    class Meta: model = Partido; fields = "__all__"

class EventoSerializer(serializers.ModelSerializer):
    class Meta: model = EventoPartido; fields = "__all__"
