from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Bodega


class ListarBodega(BaseCommand):
    # def __init__(self, request_body: dict):
    #     self.bodega_template = request_body

    def execute(self):

        try:
        
            bodegas = Bodega.query.all()

            if not bodegas:
                return {
                    "response": {
                        "msg": "No hay bodegas registradas."
                    },
                    "status_code": 201
                }

            bodegas_list = []
            for bodega in bodegas:
                bodegas_list.append({
                    "id": bodega.id,
                    "nombre": bodega.nombre,
                    "direccion": bodega.direccion,
                    "latitude": bodega.latitude,
                    "longitude": bodega.longitude,
                })

            return {
                "response": {
                    "bodegas": bodegas_list
                },
                "status_code": 200
            }
        
        except Exception as e:

            return {
                "response": {
                    "msg": "Problemas con la conexión a la base de datos.",
                },
                "status_code": 500
            }
    