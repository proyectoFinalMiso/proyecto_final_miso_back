from src.commands.base_command import BaseCommand
from src.models.model import Producto


class ListarProductos(BaseCommand):
    def buscar_productos(self) -> bool:
        return Producto.query.all()

    def execute(self):
        productos = self.buscar_productos()

        if not productos:
            return {
                "response": {"msg": "No se han encontrado productos registrados en la plataforma"},
                "status_code": 404,
            }
        return {
            "response": {"msg": "Lista de productos", "body": productos},
            "status_code": 200,
        }