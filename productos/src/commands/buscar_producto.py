from sqlalchemy import or_, cast, String
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

        clave = self.body['clave']
        clave_str = str(clave)
        clave_like = f"%{clave_str}%"

        productos = db.session.query(
            Producto.id,
            Producto.nombre,
            Producto.sku,
            Producto.volumen,
            Producto.valorUnitario,
            Producto.fechaCreacion,
            Producto.fabricante,
            Fabricante.nombre.label("fabricante_nombre")
            ).join(Fabricante).filter(
                or_(
                    cast(Producto.sku, String).ilike(clave_like),
                    Producto.nombre.ilike(clave_like),
                )
            ).all()
        
        return productos
        


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
                "id_fabricante": producto.fabricante,
                "fabricante": producto.fabricante_nombre,
                "valorUnitario": producto.valorUnitario,
                "fechaCreacion": producto.fechaCreacion,
            }
            for producto in productos
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
