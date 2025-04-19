from datetime import datetime, timezone
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity

db = SQLAlchemy()


class EstadoPedido(Enum):
    SOLICITADO = "SOLICITADO"
    EN_PROCESO = "EN_PROCESO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.String, primary_key=True)
    packingList = db.Column(db.String, nullable=False)
    cliente = db.Column(db.String, nullable=False)
    vendedor = db.Column(db.String, nullable=False)
    fechaIngreso = db.Column(db.DateTime, nullable=False)
    direccion = db.Column(db.String, nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    estado = db.Column(db.Enum(EstadoPedido), nullable=False)
    valorFactura = db.Column(db.Float, nullable=False)


class PackingList(db.Model):
    __tablename__ = 'packingLists'
    id = db.Column(db.Integer, Identity(start=1, cycle=True),
                   nullable=False, primary_key=True)
    listID = db.Column(db.String)
    producto = db.Column(db.String, nullable=False)
    cantidad = db.Column(db.String, nullable=False)
    costoTotal = db.Column(db.Float, nullable=False)


class RutaDeEntrega(db.Model):
    __tablename__ = 'rutaDeEntrega'
    id = db.Column(db.Integer, Identity(start=1, cycle=True),
                   nullable=False, primary_key=True)
    pedidoID = db.Column(db.String)
    ruta = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)