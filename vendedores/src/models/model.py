from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity

db = SQLAlchemy()

class Vendedor(db.Model):
    __tablename__ = 'vendedores'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    contrasena = db.Column(db.String, nullable=False)

class EstadoPlan(Enum):
    INICIADO = "INICIADO"
    FINALIZADO = "FINALIZADO"

class PlanVentas(db.Model):
    __tablename__ = 'planVentas'

    id = db.Column(db.String, primary_key=True)
    vendedor_id = db.Column(db.String, db.ForeignKey('vendedores.id'), nullable=False)
    vendedor_nombre = db.Column(db.String, nullable=False)
    estado = db.Column(db.Enum(EstadoPlan), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.now())
    fecha_final = db.Column(db.DateTime, nullable=True)
    meta_ventas = db.Column(db.Integer, nullable=False)
    productos_plan = db.Column(db.String, nullable=False)
    # productosVendidos = db.Column(db.String, nullable=False)

# class ReporteVendedores(db.Model):
#     __tablename__ = 'reporte_vendedores'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     vendedor_id = db.Column(db.String, db.ForeignKey('vendedores.id'), nullable=False)
#     estado = db.Column(db.Enum(EstadoPlan), nullable=False)
#     fechaInicio = db.Column(db.DateTime, default=datetime.now())
#     fechaFinal = db.Column(db.DateTime, nullable=False)
#     metaVentas = db.Column(db.Integer, nullable=False)

#     vendedor = db.relationship('Vendedor', backref='reportes')