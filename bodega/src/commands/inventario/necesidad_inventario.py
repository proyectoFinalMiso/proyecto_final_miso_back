from src.commands.base_command import BaseCommand

from src.models.model import db, NecesidadCompras

class NecesidadInventario(BaseCommand):

    def execute(self):

        try: 
            necesidad_inventario = NecesidadCompras.query.all()

            if not necesidad_inventario:
                return {
                    "response": {
                        "msg": "No hay necesidades de inventario registradas."
                    },
                    "status_code": 200
                }

            return {
                "response": {
                    "msg": "Necesidades de inventario encontradas.",
                    "data": [necesidad.to_dict() for necesidad in necesidad_inventario]
                }
            }
        
        except Exception as e:
            return {
                "response": {
                    "msg": f"Error al obtener las necesidades de inventario: {e}"
                },
                "status_code": 500
            }