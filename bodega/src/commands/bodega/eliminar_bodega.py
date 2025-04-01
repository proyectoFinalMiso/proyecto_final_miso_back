from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Bodega

class EliminarBodega(BaseCommand):
    def __init__(self, request_body: dict):
        self.bodega_template = request_body

    def check_campos_requeridos(self) -> bool:

        required_fields = ['id']

        if not all(field in self.bodega_template for field in required_fields):
            return False

        if not all(self.bodega_template.get(field) for field in required_fields):
            return False

        return True
    
    def verificar_bodega_existe(self) -> bool:
        
        existe_bodega_query = Bodega.query.filter(
            Bodega.id == self.bodega_template['id']
        ).first()

        if existe_bodega_query:
            return existe_bodega_query
        else:
            return False
        
    def execute(self):

        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
        
        bodega = self.verificar_bodega_existe()

        if not bodega:
            return {
                "response": {
                    "msg": "La bodega no existe."
                },
                "status_code": 409
            }
        
        try:
            db.session.delete(bodega)
            db.session.commit()

            return {
                "response": {
                    "msg": "Bodega eliminada correctamente"
                },
                "status_code": 200
            }

        except Exception as e:

            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al crear bodega"
                },
                "status_code": 500
            }