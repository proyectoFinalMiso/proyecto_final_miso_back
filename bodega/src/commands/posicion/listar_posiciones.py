from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Posicion

class ListarPosicion(BaseCommand):

    def execute(self):

        try:
            posiciones = Posicion.query.all()

            if not posiciones:
                return {
                    "response": {
                        "msg": "No hay posiciones registradas."
                    },
                    "status_code": 201
                }

            posiciones_list = []
            for posicion in posiciones:
                posiciones_list.append({
                    "id": posicion.id,
                    "nombre_posicion": posicion.nombre_posicion,
                    "bodega": posicion.bodega,
                    "volumen": posicion.volumen
                })

            return {
                "response": {
                    "posiciones": posiciones_list
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