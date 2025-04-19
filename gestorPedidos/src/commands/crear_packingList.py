from os import getenv
from uuid import uuid4, UUID

from src.adapters.adaptador_productos import AdaptadorProductos
from src.commands.base_command import BaseCommand
from src.models.model import db, PackingList


class CrearPackingList(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body

    def verificar_id_existe(self, id: UUID) -> bool:
        existe_id_query = PackingList.query.filter((PackingList.listID == id)).first()
        if existe_id_query:
            return True
        else:
            return False

    def crear_uuid(self) -> str:
        return str(uuid4())

    def validar_productos_existen(self, lista_productos: list) -> bool:
        productos = []
        adaptador = AdaptadorProductos(getenv("MS_PRODUCTOS_URL"))
        for producto in lista_productos:
            producto_existente = adaptador.confirmar_producto_existe(producto['sku'])
            if not producto_existente:
                productos.append(False)
            else:
                producto['costoTotal'] = producto['cantidad'] * producto_existente['valorUnitario']
                productos.append(producto)
        return productos

    def execute(self):
        lista_productos = self.body

        productos = self.validar_productos_existen(lista_productos)
        if not all(productos):
            return {
                "response": {"msg": "Hay productos que no existen en el sistema"},
                "status_code": 400,
            }

        id_unico = False
        while not id_unico:
            id_packingList = self.crear_uuid()
            if not self.verificar_id_existe(id_packingList):
                id_unico = True

        valorFactura = 0
        for producto in productos:
            valorFactura += producto["costoTotal"]
            posicion = PackingList(
                listID=id_packingList,
                producto=producto["sku"],
                cantidad=producto["cantidad"],
                costoTotal=producto["costoTotal"]
            )
            db.session.add(posicion)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {
                    "response": {"msg": f"Error al crear un nuevo producto: {str(e)}"},
                    "status_code": 500,
                }
        return {
            "response": {"msg": "Packing list creado con exito", "body": {"listID": id_packingList, "valorFactura": valorFactura}},
            "status_code": 201,
        }
