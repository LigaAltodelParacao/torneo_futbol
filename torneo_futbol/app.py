from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///torneo_completo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# MODELOS
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    equipos = db.relationship('Equipo', backref='categoria', lazy=True)

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    jugadores = db.relationship('Jugador', backref='equipo', lazy=True)

class Jugador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    dni = db.Column(db.String(20))
    birth_date = db.Column(db.String(20))
    team_id = db.Column(db.Integer, db.ForeignKey('equipo.id'))

class Partido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('equipo.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('equipo.id'))
    fecha = db.Column(db.String(20))
    cancha = db.Column(db.String(50))
    home_score = db.Column(db.Integer, default=0)
    away_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pendiente')  # pendiente, en_curso, finalizado
    eventos = db.relationship('Evento', backref='partido', lazy=True)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('partido.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('jugador.id'), nullable=True)
    tipo = db.Column(db.String(20))  # gol, E/C, amarilla, roja
    minuto = db.Column(db.Integer)

# CREAR TABLAS Y EJEMPLO
with app.app_context():
    db.create_all()
    if Categoria.query.count() == 0:
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

        j1 = Jugador(first_name="Juan", last_name="Perez", dni="12345678", birth_date="1990-01-01", team_id=eq1.id)
        j2 = Jugador(first_name="Maria", last_name="Gomez", dni="87654321", birth_date="1992-02-02", team_id=eq2.id)
        j3 = Jugador(first_name="Ana", last_name="Lopez", dni="11223344", birth_date="1991-03-03", team_id=eq3.id)
        j4 = Jugador(first_name="Luis", last_name="Diaz", dni="44332211", birth_date="1993-04-04", team_id=eq4.id)
        db.session.add_all([j1,j2,j3,j4])
        db.session.commit()

# RUTAS PRINCIPALES
@app.route('/')
def index():
    categorias = Categoria.query.all()
    return render_template("index.html", categorias=categorias)

@app.route('/categoria/<int:id>')
def ver_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return render_template("categoria_detalle.html", categoria=categoria)

@app.route('/partido/<int:id>')
def ver_partido(id):
    partido = Partido.query.get_or_404(id)
    jugadores_local = Jugador.query.filter_by(team_id=partido.home_team_id).all()
    jugadores_visitante = Jugador.query.filter_by(team_id=partido.away_team_id).all()
    return render_template("partido.html", partido=partido, jugadores_local=jugadores_local, jugadores_visitante=jugadores_visitante)

@app.route('/iniciar_partido/<int:id>', methods=['POST'])
def iniciar_partido(id):
    partido = Partido.query.get_or_404(id)
    partido.status = 'en_curso'
    db.session.commit()
    emit('iniciar', {'partido_id': id}, broadcast=True)
    return jsonify({'ok': True})

@app.route('/agregar_evento/<int:id>', methods=['POST'])
def agregar_evento(id):
    partido = Partido.query.get_or_404(id)
    data = request.json
    player_id = data.get('player_id')
    tipo = data.get('tipo')
    minuto = data.get('minuto')
    if not player_id and tipo != "E/C":
        return jsonify({'error': 'Jugador obligatorio'}), 400
    evento = Evento(partido_id=id, player_id=player_id, tipo=tipo, minuto=minuto)
    db.session.add(evento)
    db.session.commit()
    emit('nuevo_evento', {'partido_id': id, 'tipo': tipo, 'minuto': minuto, 'player_id': player_id}, broadcast=True)
    return jsonify({'ok': True})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
