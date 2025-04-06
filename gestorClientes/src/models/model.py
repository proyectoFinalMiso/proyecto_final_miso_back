from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    correo = db.Column(db.String, nullable=False)
    vendedorAsociado = db.Column(db.String, nullable=True) 
    contrasena = db.Column(db.String, nullable=False)
