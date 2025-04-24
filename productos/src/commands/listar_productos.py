from os import getenv

from src.commands.base_command import BaseCommand
from src.models.model import Producto, Fabricante, db
from src.adapters.adaptador_bodega import AdaptadorBodega

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
    
    def extraer_existencias(self):
        adaptador = AdaptadorBodega(getenv("MS_BODEGA_URL"))
        existencias = adaptador.listar_existencias()
        return existencias
    
    def extraer_necesidad(self):
        adaptador = AdaptadorBodega(getenv("MS_BODEGA_URL"))
        necesidad = adaptador.listar_necesidad()
        return necesidad

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
        existencias = self.extraer_existencias()
        necesidad = self.extraer_necesidad()
        productos_final = []

        for producto in productos_serializado:
            existencia_producto = 0
            necesidad_producto = 0
            for sku in existencias:
                if producto['sku'] == sku['sku']:
                    existencia_producto = sku['existencia']
            for sku in necesidad:
                if producto['sku'] == sku['sku']:
                    necesidad_producto = sku['cantidad']
            producto['existencia'] = existencia_producto
            producto['necesidad'] = necesidad_producto
            productos_final.append(producto)

        if not productos:
            return {
                "response": {"msg": "No se han encontrado productos registrados en la plataforma"},
                "status_code": 404,
            }
        return {
            "response": {"msg": "Lista de productos", "body": productos_final},
            "status_code": 200,
        }