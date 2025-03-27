from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity

db = SQLAlchemy()

class Fabricante(db.Model):
    __tablename__ = 'fabricantes'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False, unique=True)
    pais = db.Column(db.String, nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.String, nullable=False, unique=True)
    sku = db.Column(db.Integer, Identity(start=10001, cycle=True), nullable=False, primary_key=True)
    lote = db.Column(db.String, nullable=True)
    nombre = db.Column(db.String, nullable=True)
    volumen = db.Column(db.Float, nullable=True)
    bodega = db.Column(db.String, nullable=True)
    posicion = db.Column(db.String, nullable=True)
    cantidadDisponible = db.Column(db.Integer, default=0)
    cantidadReservada = db.Column(db.Integer, default=0)
    valorUnitario = db.Column(db.Float, nullable=False)
    fechaCreacion = db.Column(db.DateTime, nullable=False, default=datetime.now())
    fabricante = db.Column(db.String, db.ForeignKey('fabricantes.id'), nullable=False)