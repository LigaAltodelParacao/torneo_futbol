from django.contrib import admin
from .models import Categoria, Equipo, Jugador, Cancha, Partido, EventoPartido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "categoria"]
    list_filter = ["categoria"]
    search_fields = ["nombre"]

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ["nombre", "equipo", "goles", "amarillas", "rojas", "suspendido"]
    list_filter = ["equipo", "suspendido"]
    search_fields = ["nombre"]

@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ["categoria","equipo_local","equipo_visitante","cancha","fecha","en_vivo","terminado","period"]
    list_filter = ["categoria","cancha","en_vivo","terminado","period"]
    search_fields = ["equipo_local__nombre","equipo_visitante__nombre"]

@admin.register(EventoPartido)
class EventoPartidoAdmin(admin.ModelAdmin):
    list_display = ["partido","jugador","tipo","minuto","creado"]
    list_filter = ["tipo","partido__categoria"]
    search_fields = ["jugador__nombre","partido__equipo_local__nombre","partido__equipo_visitante__nombre"]
