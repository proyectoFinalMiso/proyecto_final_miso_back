from src.commands.base_command import BaseCommand
from src.models.model import db, Vendedor
from flask import jsonify


class ListarVendedores(BaseCommand):
    def buscar_vendedores(self) -> list:
        vendedores = Vendedor.query.all()
        if not vendedores:
            return False
        print(vendedores)
        return [
            {
                "id": vendedor.id,
                "nombre": vendedor.nombre,
                "email": vendedor.email,
            }
            for vendedor in vendedores
        ]

    def execute(self):
        try:
            vendedores = self.buscar_vendedores()
            if not vendedores:
                return {
                    "response": {
                        "msg": "No hay vendedores disponibles",
                    },
                    "status_code": 404,
                }
            return {
                "response": {
                    "msg": "Lista de vendedores",
                    "body": vendedores,
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