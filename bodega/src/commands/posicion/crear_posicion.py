from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Posicion, Bodega

class CrearPosicion(BaseCommand):

    def __init__(self, request_body: dict):
        self.posicion_template = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:

        required_fields = ['bodega', 'volumen']

        if not all(field in self.posicion_template for field in required_fields):
            return False

        if not all(self.posicion_template.get(field) for field in required_fields):
            return False

        return True
        
    def verificar_bodega_existe(self) -> bool:
        existe_bodega_query = Bodega.query.filter(
            Bodega.id == self.posicion_template['bodega']
        ).first()
        if existe_bodega_query:
            return True
        else:
            return False
        
    def agregar_posicion_a_bodega(self, id_posicion: str, id_bodega: str):
        
        bodega = Bodega.query.filter(Bodega.id == id_bodega).first()

        if not bodega.posiciones:
            bodega.posiciones = []

        bodega.posiciones = bodega.posiciones + [id_posicion]
        db.session.commit()

    def execute(self):

        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
        
        if not self.verificar_bodega_existe():
            return {
                "response": {
                    "msg": "La bodega no existe."
                },
                "status_code": 404
            }
        
        id_posicion = self.crear_uuid()

        nueva_posicion = Posicion(
            id=id_posicion,
            bodega=self.posicion_template['bodega'],
            volumen=self.posicion_template['volumen']
        )

        try:
            self.agregar_posicion_a_bodega(id_posicion, self.posicion_template['bodega'])
        
        except Exception as e:
            return {
                "response": {
                    "msg": "Error al agregar la posicion a la bodega",
                },
                "status_code": 500
            }

        db.session.add(nueva_posicion)

        try:
            db.session.commit()

            return {
                "response": {
                    "msg": "Posicion creada correctamente",
                    "id": nueva_posicion.id,
                    "bodega": nueva_posicion.bodega,
                    "volumen": nueva_posicion.volumen
                },
                "status_code": 201
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al crear la posicion",
                },
                "status_code": 500
            }