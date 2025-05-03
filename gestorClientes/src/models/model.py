from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy import Identity

db = SQLAlchemy()

class EstadoVisita(Enum):
    PROGRAMADA = "programada"
    COMPLETADA = "completada" 
    CANCELADA = "cancelada"

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    correo = db.Column(db.String, nullable=False)
    vendedorAsociado = db.Column(db.String, nullable=True) 
    contrasena = db.Column(db.String, nullable=False)

class Visita(db.Model):
    __tablename__ = 'visitas'

    id = db.Column(db.Integer, Identity(start=1), primary_key=True, nullable=False)
    cliente_id = db.Column(db.String, db.ForeignKey('clientes.id'), nullable=False)
    vendedor_id = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Enum(EstadoVisita), nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('visitas', lazy=True))
