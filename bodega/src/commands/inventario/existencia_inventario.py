from sqlalchemy import func

from src.commands.base_command import BaseCommand
from src.models.model import db, Inventario

class ExistenciaInventario(BaseCommand):

    def execute(self):
        
        try:

            existencia_inventario = db.session.query(
                Inventario.sku.label('sku'),
                (func.sum(Inventario.cantidadDisponible) + func.sum(Inventario.cantidadReservada)).label('cantidadTotal')
                ).group_by(Inventario.sku).all()
            
            if not existencia_inventario:
                return {
                    "response": {
                        "msg": "No se encontraron registros de inventario.",
                    },
                    "status_code": 200,
                }
            
            return {
                "response": {
                    "msg": "Consulta exitosa.",
                    "data": [existencia.to_dict() for existencia in existencia_inventario]
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
