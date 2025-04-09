from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Inventario

class IngresarInventario(BaseCommand):

    def __init__(self, request_body: dict):
        self.inventario_template = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:

        required_fields = ['sku', 'lote', 'cantidad']

        if not all(field in self.inventario_template for field in required_fields):
            return False

        if not all(self.inventario_template.get(field) for field in required_fields):
            return False

        return True
    
    def verificar_producto_existe(self) -> bool:
        existe_producto_query = Inventario.query.filter(
            Inventario.sku == self.inventario_template['sku'],
            Inventario.lote == self.inventario_template['lote'],
        ).first()
        if existe_producto_query:
            return True
        else:
            return False
        
    def verificar_cantidad(self) -> bool:
        if self.inventario_template['cantidad'] <= 0:
            return False
        else:
            return True
        
    def execute(self):
        
        if not self.check_campos_requeridos():
            return {
                "response": {
                    'msg': 'Faltan campos requeridos'
                },
                "status_code": 400
            }

        if not self.verificar_producto_existe():
            return {
                "response": {
                    'msg': 'El producto no existe'
                }, 
            "status_code": 404
            }

        if not self.verificar_cantidad():
            return  {
                "response": {
                    'msg': 'La cantidad debe ser mayor a 0'
                },
            "status_code": 400
            }

        try:
            producto = Inventario.query.filter(
                Inventario.sku == self.inventario_template['sku'],
                Inventario.lote == self.inventario_template['lote']).first()
            if producto:
                producto.cantidadDisponible += self.inventario_template['cantidad']
                db.session.commit()

            return {
                "response": {
                    "msg": "Inventario actualizado correctamente"
                },
                "status_code": 200
            }

        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al cambiar antidades del producto"
                },
                "status_code": 500
            }
        