from src.commands.base_command import BaseCommand
from src.models.model import db, Posicion

class BuscarPosicion(BaseCommand):

    def __init__(self, request_body: dict):
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        if self.body.get("id_posicion"):
            return True
        else:
            return False
        
    def buscar_posicion(self) -> bool:
        id_posicion = f"%{self.body['id_posicion']}%"
        return db.session.query(Posicion).filter(
            Posicion.id.ilike(id_posicion)
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