from sqlalchemy import or_

from src.commands.base_command import BaseCommand
from src.models.model import db, Bodega

class BuscadorBodega(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        if self.body.get("clave"):
            return True
        else:
            return False

    def buscar_bodegas(self) -> bool:

        clave = f"%{self.body['clave']}%"

        return db.session.query(Bodega).filter(
            or_(
                Bodega.nombre.ilike(clave),
                Bodega.direccion.ilike(clave),
                Bodega.id.ilike(clave)
            )
        ).all()
    
    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Clave para buscar bodega no valida"
                },
                "status_code": 400,
            }
        
        try:
            
            bodegas = self.buscar_bodegas()

            bodegas_serializado = [
                {
                    "id": bodega.id,
                    "nombre": bodega.nombre,
                    "direccion": bodega.direccion,
                    "posicion": bodega.posiciones if bodega.posiciones else "Aun no tiene posiciones"
                }
                for bodega in bodegas
            ]
            print(bodegas_serializado)
            if not bodegas:
                return {
                    "response": {"msg": "No se ha encontrado la bodega solicitada"},
                    "status_code": 404,
                }

            return {
                "response": {
                    "bodegas": bodegas_serializado
                },
                "status_code": 200,
            }
        
        except Exception as e:
            return {
                "response": {
                    "msg": "Problemas con la conexión a la base de datos.",
                },
                "status_code": 500
            }