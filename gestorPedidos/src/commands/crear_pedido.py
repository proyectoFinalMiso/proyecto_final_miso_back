from datetime import datetime
from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.commands.crear_packingList import CrearPackingList
from src.models.model import db, Pedido, EstadoPedido

class CrearPedido(BaseCommand):

    def __init__(self, request_body: dict):
        self.body = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:
        required_fields = [
            "cliente",
            "vendedor",
            "direccion",
            "latitud",
            "longitud",
            "productos"
        ]

        if not all(field in self.body for field in required_fields):
            return False

        if not all(self.body.get(field) for field in required_fields):
            return False

        return True
    
    def generar_nuevo_packing_list(self):
        posiciones = self.body['productos']
        response = CrearPackingList(posiciones).execute()
        packing_list = response['response']['body']
        return packing_list
    
    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
        
        id_pedido = self.crear_uuid()
        packing_list = self.generar_nuevo_packing_list()

        nuevo_pedido = Pedido(
            id=id_pedido,
            packingList=packing_list['listID'],
            cliente=self.body['cliente'],
            vendedor=self.body['vendedor'],
            direccion=self.body['direccion'],
            latitud=self.body['latitud'],
            longitud=self.body['longitud'],
            fechaIngreso=datetime.now(),
            estado=EstadoPedido.SOLICITADO.value,
            valorFactura=packing_list['valorFactura']
        )
        db.session.add(nuevo_pedido)

        try:            
            db.session.commit()
            return {
                "response": {
                    "msg": "Pedido creado con exito"
                },
                "status_code": 201
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al crear pedido"
                },
                "status_code": 500
            }
