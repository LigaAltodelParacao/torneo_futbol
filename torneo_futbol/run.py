from app import app, db
from app import Categoria, Equipo, Jugador, Partido, Evento

with app.app_context():
    # Crear la base de datos y tablas si no existen
    print("Creando la base de datos y tablas...")
    db.create_all()
    print("Base de datos lista.")

    # Opcional: agregar algunas categorías y equipos de ejemplo si no existen
    if Categoria.query.count() == 0:
        print("Agregando datos de ejemplo...")
        cat1 = Categoria(name="M30 A")
        cat2 = Categoria(name="Femenina B")
        db.session.add_all([cat1, cat2])
        db.session.commit()
        
        eq1 = Equipo(name="Equipo 1", category_id=cat1.id)
        eq2 = Equipo(name="Equipo 2", category_id=cat1.id)
        eq3 = Equipo(name="Equipo 3", category_id=cat2.id)
        eq4 = Equipo(name="Equipo 4", category_id=cat2.id)
        db.session.add_all([eq1, eq2, eq3, eq4])
        db.session.commit()
        print("Datos de ejemplo agregados.")

# Ejecutar el servidor Flask + SocketIO
print("Iniciando servidor...")
from flask_socketio import SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")
socketio.run(app, host="0.0.0.0", port=5000)
