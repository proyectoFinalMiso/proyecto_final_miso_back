import string
from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Bodega

class CrearBodega(BaseCommand):
    
    def __init__(self, request_body: dict):
        self.bodega_template = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:

        required_fields = ['nombre', 'direccion', 'latitude', 'longitude']

        if not all(field in self.bodega_template for field in required_fields):
            return False

        if not all(self.bodega_template.get(field) for field in required_fields):
            return False

        return True
    
    def verificar_bodega_existe(self) -> bool:
        
        existe_bodega_query = Bodega.query.filter(
            Bodega.nombre == self.bodega_template['nombre']
        ).first()

        if existe_bodega_query:
            return True
        else:
            return False
        
    def crear_posiciones(self):

        valores = [f"{letra}{numero}" for letra in string.ascii_uppercase for numero in range(1, 4)]

        return valores

    
    def execute(self):
        
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
        
        if self.verificar_bodega_existe():
            return {
                "response": {
                    "msg": "La bodega ya existe."
                },
                "status_code": 409
            }
        
        posiciones = self.crear_posiciones()
        
        id_bodega = self.crear_uuid()

        nueva_bodega = Bodega(
            id=id_bodega,
            nombre=self.bodega_template['nombre'],
            posiciones=posiciones,
            direccion=self.bodega_template['direccion'],
            latitude=self.bodega_template['latitude'],
            longitude=self.bodega_template['longitude'],
        )
        db.session.add(nueva_bodega)

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Bodega creada exitosamente",
                    "bodega": {
                        "id": id_bodega,
                        "nombre": self.bodega_template['nombre'],
                        "direccion": self.bodega_template['direccion']
                    }
                },
                "status_code": 201
            }
        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al crear bodega"
                },
                "status_code": 500
            }