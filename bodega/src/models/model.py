from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Bodega(db.Model):
    __tablename__ = 'bodega'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    posiciones = db.Column(JSON, nullable=True, default=list)
    direccion = db.Column(db.String, nullable=False)

class Posicion(db.Model):
    __tablename__ = 'posicion'

    id = db.Column(db.String, primary_key=True)
    bodega = db.Column(db.String, db.ForeignKey('bodega.id'), nullable=False)
    volumen = db.Column(db.Float, nullable=False)
    productos = db.Column(JSON, nullable=True, default=list)

class Inventario(db.Model):
    __tablename__ = 'inventario'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    bodega = db.Column(db.String, db.ForeignKey('bodega.id'), nullable=False)
    posicion = db.Column(db.String, db.ForeignKey('posicion.id'), nullable=False)
    lote = db.Column(db.String, nullable=False)
    cantidadDisponible = db.Column(db.Integer, nullable=False)
    cantidadReservada = db.Column(db.Integer, default=0)
    fechaIgreso = db.Column(db.DateTime, nullable=False)
    sku = db.Column(db.Integer, Identity(start=10001, cycle=True), nullable=False)