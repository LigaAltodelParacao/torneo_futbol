# Torneo de Fútbol (Django + DRF + Channels)

## Requisitos
- Python 3.10+ (recomendado)
- (Opcional para producción) Redis si querés usar channels_redis

## Instalación
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python scripts/load_defaults.py
python manage.py runserver
```

## Rutas
- Admin: `/admin/`
- API CRUD (DRF): `/api/`
- Importar jugadores (POST, admin): `/api/import/jugadores/` (form-data file=`file` con columnas: **Nombre**, **Equipo**)
- Tablas: `/api/tablas/goleadores/`, `/api/tablas/fairplay/`, `/api/tablas/suspensiones/`, `/api/tablas/posiciones/`
- UI:
  - Partidos en vivo: `/api/ui/live/`
  - Viewer: `/api/ui/partido/<id>/`
  - Control Admin: `/api/ui/admin/partido/<id>/`
- WebSocket: `ws://host/ws/partido/<id>/`

### Nota sobre Channels
En `settings.py` el layer es **InMemory** para que funcione sin Redis en dev.
Si querés usar Redis, descomentá la config de `CHANNEL_LAYERS` y agregá `channels_redis` en `requirements.txt`.
