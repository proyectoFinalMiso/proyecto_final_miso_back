import re
from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Vendedor

class ObtenerVendedor(BaseCommand):

    def __init__(self, vendedor_id: str):
        self.vendedor_id = vendedor_id
        
    def verificar_vendedor_existe(self):
        vendedor_query = Vendedor.query.filter_by(id=self.vendedor_id).first()

        if vendedor_query:
            return vendedor_query
        else:
            return False
        
    def execute(self):
        info_vendedor = self.verificar_vendedor_existe()

        if not info_vendedor:
            return {
                "response": {
                    "msg": "Vendedor no existe"
                },
                "status_code": 404
            }
        
        return {
            "response": {
                "id": f"{info_vendedor.id}",
                "nombre": f"{info_vendedor.nombre}",
                "email": f"{info_vendedor.email}"
            },
            "status_code": 200
        }
