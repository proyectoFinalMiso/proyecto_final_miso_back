from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Fabricante

class CrearFabricante(BaseCommand):

    def __init__(self, request_body: dict):
        self.fabricante_template = request_body

    def verificar_fabricante_existe(self) -> bool:

        existe_fabricante_query = Fabricante.query.filter(
            (Fabricante.nombre == self.fabricante_template['nombre'])
            & (Fabricante.pais == self.fabricante_template['pais'])
        ).first()

        if existe_fabricante_query:
            return True
        else:
            return False
        
    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:

        if self.fabricante_template.get('nombre') and self.fabricante_template.get('pais'):
            return True
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
        
        if self.verificar_fabricante_existe():
            return {
                "response": {
                    "msg": "Fabricante ya existe"
                },
                "status_code": 400
            }
        
        id_fabricante = self.crear_uuid()

        nuevo_fabricante = Fabricante(
            id=id_fabricante,
            nombre=self.fabricante_template['nombre'],
            pais=self.fabricante_template['pais']
        )

        db.session.add(nuevo_fabricante)

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Fabricante creado con exito",
                    "id": f"{id_fabricante}"
                },
                "status_code": 201
            }
        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": f"Error al crear fabricante: {str(e)}"
                },
                "status_code": 500
            }
        
    