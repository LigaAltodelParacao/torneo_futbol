import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torneo_futbol.settings')
django.setup()
from torneos.models import Cancha, Categoria

canchas = [f"Parera - Cancha {i}" for i in range(1,12)] + [f"Ramírez - Cancha {i}" for i in range(1,7)]
for c in canchas:
    Cancha.objects.get_or_create(nombre=c)

for cat in ["M30 A", "M30 B", "Libre", "Femenino"]:
    Categoria.objects.get_or_create(nombre=cat)

print("Canchas y categorías cargadas.")
