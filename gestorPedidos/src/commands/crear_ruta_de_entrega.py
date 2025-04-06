from uuid import uuid4

import requests
from src.commands.base_command import BaseCommand
from src.commands.crear_packingList import CrearPackingList
from src.constants.urls import PRODUCT_URL
from src.models.model import PackingList, Pedido, db


class CrearRutaDeEntrega(BaseCommand):

    def __init__(self, request_body: dict):
        self.body = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())

    def check_campos_requeridos(self) -> bool:
        required_fields = ["pedido_id"]

        if not all(field in self.body for field in required_fields):
            return False

        if not all(self.body.get(field) for field in required_fields):
            return False

        return True

    def obtener_producto_por_sku(self, sku):
        obtener_producto_url = PRODUCT_URL + "/producto/buscar_sku"
        payload = {"clave": sku}
        headers = {
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                obtener_producto_url, json=payload, headers=headers)
            if response.status_code not in [200, 201]:
                raise Exception(f"Error al obtener producto: "
                                f"Status {response.status_code} - {response.text}")
            return response.json()
        except requests.RequestException as e:
            raise Exception(
                f"Error de conexión al hacer POST a {obtener_producto_url}: {str(e)}")

    def execute(self):
        pedido_id = self.body["pedido_id"]

        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }

        productos = []

        pedido_obtenido = Pedido.query.filter_by(id=pedido_id).first()
        print(pedido_obtenido)

        packing_list_id = pedido_obtenido.packingList
        print(packing_list_id)

        packing_list_obtenido = PackingList.query.filter_by(
            listID=packing_list_id).all()
        print(packing_list_obtenido)

        for p in packing_list_obtenido:
            sku = p.producto
            print(sku)
            busqueda_de_producto = self.obtener_producto_por_sku(sku)
            print(busqueda_de_producto)
            productos.append(busqueda_de_producto)

        print(productos)

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Ruta de entrega creada con exito"
                },
                "status_code": 201
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "response": {
                    "msg": f"Error al crear ruta de entrega para el pedido {pedido_id}"
                },
                "status_code": 500
            }
