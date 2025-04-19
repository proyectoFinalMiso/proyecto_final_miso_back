from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Identity

db = SQLAlchemy()

class Vendedor(db.Model):
    __tablename__ = 'vendedores'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    contrasena = db.Column(db.String, nullable=False)
