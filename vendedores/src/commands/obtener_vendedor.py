import re
from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Vendedor

class ObtenerVendedor(BaseCommand):

    def __init__(self, request_body: dict):
        self.vendedor_template = request_body

    def check_campos_requeridos(self) -> bool:
        if self.vendedor_template.get('email'):
            return True
        else:
            return False
        
    def verificar_vendedor_existe(self) -> bool:

        vendedor_query = Vendedor.query.filter(
            Vendedor.email == self.vendedor_template['email']
        ).first()

        if vendedor_query:
            return vendedor_query
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
        
        info_vendedor = self.verificar_vendedor_existe()
        print(type(info_vendedor))
        print(info_vendedor)
        print(info_vendedor.id)
        print(info_vendedor.nombre)
        print(info_vendedor.email)
        
        if not info_vendedor:
            return {
                "response": {
                    "id": "Vendedor no existe"
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