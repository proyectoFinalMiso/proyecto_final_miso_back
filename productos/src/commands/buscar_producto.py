from src.commands.base_command import BaseCommand
from src.models.model import Producto


class BuscarProducto(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        if self.body.get("sku"):
            return True
        else:
            return False

    def buscar_producto(self) -> bool:
        return Producto.query.filter((Producto.sku == self.body["sku"])).first()

    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Solo se pueden buscar productos por medio del SKU"
                },
                "status_code": 400,
            }

        producto = self.buscar_producto()

        if not producto:
            return {
                "response": {"msg": "No se ha encontrado el producto solicitado"},
                "status_code": 404,
            }
        producto = producto.__dict__
        del producto["_sa_instance_state"]
        return {
            "response": {"msg": "Producto encontrado", "body": producto},
            "status_code": 200,
        }
