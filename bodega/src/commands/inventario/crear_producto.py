from uuid import uuid4

from src.commands.base_command import BaseCommand
from src.models.model import db, Inventario, Posicion, Bodega
from datetime import datetime

class CrearProducto(BaseCommand):

    def __init__(self, request_body: dict):
        self.producto_template = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:

        required_fields = ['nombre', 'valorUnitario', 'bodega', 'lote', 'cantidad', 'sku']

        if not all(field in self.producto_template for field in required_fields):
            return False

        if not all(self.producto_template.get(field) for field in required_fields):
            return False

        return True
        
    def verificar_bodega_existe(self) -> bool:
        existe_bodega_query = Bodega.query.filter(
            Bodega.nombre == self.producto_template['bodega']
        ).first()
        if existe_bodega_query:
            return True
        else:
            return False
        
    def obtener_id_bodega(self) -> str:
        existe_bodega_query = Bodega.query.filter(
            Bodega.nombre == self.producto_template['bodega']
        ).first()

        if existe_bodega_query:
            return existe_bodega_query.id
        else:
            return None
        
    def definir_posicion(self) -> str:
        existe_posicion_query = Posicion.query.filter(
            Posicion.volumen >= 100.0,
            (Posicion.productos == '') | (Posicion.productos == [])
        ).first()

        if existe_posicion_query:
            return {
                'id': existe_posicion_query.id,
                'nombre_posicion': existe_posicion_query.nombre_posicion,
            }
        else:
            return False
        
    # def verificar_posicion_existe(self) -> bool:
    #     existe_posicion_query = Posicion.query.filter(
    #         Posicion.nombre_posicion == self.producto_template['posicion'],
    #         Posicion.bodega == self.producto_template['bodega']
    #     ).first()
    #     if existe_posicion_query:
    #         return True
    #     else:
    #         return False
        
    # def obtener_id_posicion(self) -> str:
    #     existe_posicion_query = Posicion.query.filter(
    #         Posicion.nombre_posicion == self.producto_template['posicion'],
    #         Posicion.bodega == self.producto_template['bodega']
    #     ).first()

    #     if existe_posicion_query:
    #         return existe_posicion_query.id
    #     else:
    #         return None
        
    def verificar_producto_existe(self) -> bool:
        existe_producto_query = Inventario.query.filter(
            Inventario.nombre == self.producto_template['nombre'],
            Inventario.bodega == self.producto_template['bodega'],
            Inventario.sku == self.producto_template['sku'],
            Inventario.lote == self.producto_template['lote']
        ).first()
        if existe_producto_query:
            return True
        else:
            return False
        
    def agregar_producto_a_posicion(self, id_producto: str, id_posicion: str):

        posicion = Posicion.query.filter(Posicion.id == id_posicion).first()
        
        if not posicion.productos:
            posicion.productos = []
        posicion.productos = posicion.productos + [id_producto]
        db.session.commit()

    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
        
        if not self.verificar_bodega_existe():
            return {
                "response": {
                    "msg": "La bodega no existe."
                },
                "status_code": 404
            }
        
        # if not self.verificar_posicion_existe():
        #     return {
        #         "response": {
        #             "msg": "La posicion no existe."
        #         },
        #         "status_code": 404
        #     }
        
        if self.verificar_producto_existe():
            return {
                "response": {
                    "msg": "El producto ya existe."
                },
                "status_code": 409
            }
        
        id_bodega = self.obtener_id_bodega()
        id_producto = self.crear_uuid()
        posicion_producto = self.definir_posicion()

        if not posicion_producto:
            return {
                "response": {
                    "msg": "No hay posiciones disponibles."
                },
                "status_code": 404
            }

        nuevo_producto = Inventario(
            id=id_producto,
            nombre=self.producto_template['nombre'],
            valorUnitario=self.producto_template['valorUnitario'],
            bodega=self.producto_template['bodega'],
            id_bodega=id_bodega,
            posicion=posicion_producto['nombre_posicion'],
            id_posicion=posicion_producto['id'],
            lote=self.producto_template['lote'],
            cantidadDisponible=self.producto_template['cantidad'],
            fechaIgreso=datetime.now(),
            sku=self.producto_template['sku']
        )

        try:
            self.agregar_producto_a_posicion(id_producto, posicion_producto['id'])
        except Exception as e:
            return {
                "response": {
                    "msg": f"Error al agregar el producto a la posicion {str(e)}",
                },
                "status_code": 500
            }
        
        db.session.add(nuevo_producto)

        try:
            
            db.session.commit()

            return {
                "response": {
                    "producto": {
                        "id": nuevo_producto.id,
                        "nombre": nuevo_producto.nombre,
                        "valorUnitario": nuevo_producto.valorUnitario,
                        "bodega": nuevo_producto.bodega,
                        "posicion": nuevo_producto.posicion,
                        "lote": nuevo_producto.lote,
                        "cantidad": nuevo_producto.cantidadDisponible,
                        "fechaIngreso": nuevo_producto.fechaIgreso,
                        "sku": nuevo_producto.sku
                    },
                    "msg": "Producto creado correctamente",
                    
                },
                "status_code": 201
            }
        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": f"Error al crear el producto {e}"
                },
                "status_code": 500
            }
