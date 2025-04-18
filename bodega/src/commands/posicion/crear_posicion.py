from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Posicion, Bodega

class CrearPosicion(BaseCommand):

    def __init__(self, request_body: dict):
        self.posicion_template = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:

        required_fields = ['nombre_posicion', 'bodega', 'volumen']

        if not all(field in self.posicion_template for field in required_fields):
            return False

        if not all(self.posicion_template.get(field) for field in required_fields):
            return False

        return True
    
        
    def verificar_bodega_existe(self) -> bool:
        existe_bodega_query = Bodega.query.filter(
            Bodega.nombre == self.posicion_template['bodega']
        ).first()
        if existe_bodega_query:
            return True
        else:
            return False
        
    def obtener_id_bodega(self) -> str:
        existe_bodega_query = Bodega.query.filter(
            Bodega.nombre == self.posicion_template['bodega']
        ).first()

        if existe_bodega_query:
            return existe_bodega_query.id
        else:
            return None
        
    def agregar_posicion_a_bodega(self, nombre_posicion: str, bodega: str):
        
        bodega = Bodega.query.filter(Bodega.nombre == bodega).first()

        if not bodega.posiciones:
            bodega.posiciones = []

        bodega.posiciones = bodega.posiciones + [nombre_posicion]
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
        
        id_bodega = self.obtener_id_bodega()
        if not id_bodega:
            return {
                "response": {
                    "msg": "Error al obtener el id de la bodega."
                },
                "status_code": 500
            }
        
        id_posicion = self.crear_uuid()

        nueva_posicion = Posicion(
            id=id_posicion,
            nombre_posicion=self.posicion_template['nombre_posicion'],
            bodega=self.posicion_template['bodega'],
            id_bodega=id_bodega,
            volumen=self.posicion_template['volumen']
        )

        try:
            self.agregar_posicion_a_bodega(self.posicion_template['nombre_posicion'], self.posicion_template['bodega'])
        
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
                    "posicion": {
                        "id": nueva_posicion.id,
                        "nombre_posicion": nueva_posicion.nombre_posicion,
                        "bodega": nueva_posicion.bodega,
                        "volumen": nueva_posicion.volumen
                    },
                    "msg": "Posicion creada correctamente",
                    
                },
                "status_code": 201
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": f"Error al crear la posicion: {str(e)}"
                },
                "status_code": 500
            }