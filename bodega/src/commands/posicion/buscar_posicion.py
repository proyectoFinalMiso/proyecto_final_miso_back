from sqlalchemy import or_

from src.commands.base_command import BaseCommand
from src.models.model import db, Posicion

class BuscarPosicion(BaseCommand):

    def __init__(self, request_body: dict):
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        if self.body.get("posicion"):
            return True
        else:
            return False
        
    def buscar_posicion(self) -> bool:
        clave = f"%{self.body['posicion']}%"
        return db.session.query(Posicion).filter(
            or_(Posicion.id.ilike(clave),
                Posicion.nombre_posicion.ilike(clave),
            )
        ).all()
    
    def execute(self):
        
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Id de posicion no valida"
                },
                "status_code": 400,
            }
        
        try:
            
            posiciones = self.buscar_posicion()

            posiciones_serializado = [
                {
                    "id": posicion.id,
                    "nombre_posicion": posicion.nombre_posicion,
                    "bodega": posicion.bodega,
                    "volumen": posicion.volumen,
                    "productos": posicion.productos if posicion.productos else "Aun no tiene productos"
                }
                for posicion in posiciones
            ]

            if not posiciones:
                return {
                    "response": {"msg": "No se ha encontrado la posicion solicitada"},
                    "status_code": 404,
                }

            return {
                "response": {
                    "posiciones": posiciones_serializado
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