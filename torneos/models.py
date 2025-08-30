from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): return self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="equipos")
    def __str__(self): return self.nombre

class Jugador(models.Model):
    nombre = models.CharField(max_length=150)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="jugadores")
    amarillas = models.IntegerField(default=0)
    rojas = models.IntegerField(default=0)
    goles = models.IntegerField(default=0)
    suspendido = models.BooleanField(default=False)
    def __str__(self): return self.nombre

class Cancha(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    def __str__(self): return self.nombre

class Partido(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    equipo_local = models.ForeignKey(Equipo, related_name="partidos_local", on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name="partidos_visitante", on_delete=models.CASCADE)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    en_vivo = models.BooleanField(default=False)
    terminado = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    period = models.IntegerField(default=0)  # 0=no iniciado,1=1er,2=descanso,3=2do,4=terminado
    minuto_actual = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.fecha}"

class EventoPartido(models.Model):
    TIPOS = [("gol","Gol"),("amarilla","Amarilla"),("roja","Roja")]
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name="eventos")
    minuto = models.IntegerField()
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="eventos")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    creado = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.tipo} - {self.jugador} ({self.minuto}')"
