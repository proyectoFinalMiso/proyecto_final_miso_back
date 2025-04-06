from src.commands.base_command import BaseCommand
from src.models.model import Producto, Fabricante, db


class ListarProductos(BaseCommand):
    def buscar_productos(self) -> bool:
        productos = db.session.query(
            Producto.id,
            Producto.nombre,
            Producto.sku,
            Producto.volumen,
            Producto.valorUnitario,
            Producto.fechaCreacion,
            Producto.fabricante,
            Fabricante.nombre.label("fabricante_nombre"),
        ).join(Fabricante).all()
        return [producto for producto in productos]

    def execute(self):
        productos = self.buscar_productos()
        productos_serializado = [
            {
                "id": producto.id,
                "nombre": producto.nombre,
                "sku": producto.sku,
                "volumen": producto.volumen,
                "id_fabricante": producto.fabricante,
                "fabricante": producto.fabricante_nombre,
                "valorUnitario": producto.valorUnitario,
                "fechaCreacion": producto.fechaCreacion,
            }
            for producto in productos
        ]

        if not productos:
            return {
                "response": {"msg": "No se han encontrado productos registrados en la plataforma"},
                "status_code": 404,
            }
        return {
            "response": {"msg": "Lista de productos", "body": productos_serializado},
            "status_code": 200,
        }