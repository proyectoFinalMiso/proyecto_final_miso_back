from sqlalchemy import or_
from src.commands.base_command import BaseCommand
from src.models.model import Producto, Fabricante, db


class BuscadorProducto(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        if self.body.get("clave"):
            return True
        else:
            return False

    def buscar_producto(self) -> bool:

        clave = f"%{self.body['clave']}%"

        return db.session.query(Producto, Fabricante.nombre).join(Fabricante).filter(
            or_(
                Producto.sku.ilike(clave),
                Producto.nombre.ilike(clave),
                Producto.fabricante.ilike(clave)
            )
        ).all()

    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Clave para buscar producto no valida"
                },
                "status_code": 400,
            }

        productos = self.buscar_producto()

        productos_serializado = [
            {
                "id": producto.id,
                "nombre": producto.nombre,
                "sku": producto.sku,
                "volumen": producto.volumen,
                "fabricante": nombre_fabricante,
                "valorUnitario": producto.valorUnitario,
                "fechaCreacion": producto.fechaCreacion,
            }
            for producto, nombre_fabricante in productos
        ]


        if not productos:
            return {
                "response": {"msg": "No se ha encontrado el producto solicitado"},
                "status_code": 404,
            }

        return {
            "response": {"body": productos_serializado},
            "status_code": 200,
        }
