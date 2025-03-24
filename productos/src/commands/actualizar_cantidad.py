from src.commands.base_command import BaseCommand
from src.models.model import Producto

class ActualizarCantidadProducto (BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        if self.body.get("nombre") and self.body.get("lote") and self.body.get("cantidad"):
            return True
        else:
            return False

    def producto_existe(self):

        return Producto.query.filter((Producto.nombre == self.body["nombre"]), (Producto.lote == self.body["lote"])).first()

    def modificar_cantidad(self):
        pass

    def execute(self):

        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Solo se pueden buscar productos por medio del SKU"
                },
                "status_code": 400,
            }
        
        if not self.producto_existe():
            return {
                "response": {
                    "msg": "Producto y lote no existe"
                },
                "status_code": 400,
            }

        
