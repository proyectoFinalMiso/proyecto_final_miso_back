from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Inventario


class ListarInventarios(BaseCommand):

    def buscar_inventarios(self) -> list:
        inventarios = Inventario.query.all()
        return [inventario.to_dict() for inventario in inventarios]

    def execute(self):

        try:
            inventarios = self.buscar_inventarios()
            if not inventarios:
                return {
                    "response": {
                        "msg": "No hay inventarios disponibles",
                    },
                    "status_code": 404,
                }
            return {
                "response": {
                    "msg": "Lista de inventarios",
                    "body": inventarios,
                },
                "status_code": 200,
            }
            
        except Exception as e:
            return {
                "response": {
                    "msg": "Problemas con la conexión a la base de datos.",
                    "error": str(e),
                },
                "status_code": 500,
            }
