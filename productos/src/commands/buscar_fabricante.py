from src.commands.base_command import BaseCommand
from src.models.model import Fabricante


class BuscarFabricante(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        if self.body.get("nombre"):
            return True
        else:
            return False

    def buscar_fabricante(self) -> bool:
        clave = self.body['nombre']
        clave_str = str(clave)
        clave_like = f"%{clave_str}%"

        fabricante = Fabricante.query.filter(Fabricante.nombre.ilike(clave_like)).first()
            
        return fabricante

    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Debe indicar el nombre del fabricante"
                },
                "status_code": 400,
            }

        fabricante = self.buscar_fabricante()

        if not fabricante:
            return {
                "response": {"msg": "No se ha encontrado el fabricante solicitado"},
                "status_code": 404,
            }

        return {
            "response": {"msg": "Fabricante encontrado", "body": fabricante.to_dict()},
            "status_code": 200,
        }
