import json
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

        required_fields = ['nombre', 
                           'valorUnitario', 
                           'bodega', 
                           'lote', 
                           'cantidad', 
                           'sku', 
                           'volumen']

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
            return False
        
    def verificar_producto_existe(self) -> bool:
        existe_producto_query = Inventario.query.filter(
            Inventario.nombre == self.producto_template['nombre'],
            Inventario.bodega == self.producto_template['bodega'],
            Inventario.sku == int(self.producto_template['sku']),
            Inventario.lote == self.producto_template['lote']
        ).first()
        if existe_producto_query:
            return True
        else:
            return False
        
    def posiciones_necesarias(self) -> int:

        volumen = float(self.producto_template['volumen'])
        cantidad = int(self.producto_template['cantidad'])

        if int((volumen * cantidad) % 100.0) == 0:
            posiciones_necesarias = 1
        else:
            posiciones_necesarias = int((volumen * cantidad) // 100.0) + 1

        return posiciones_necesarias
        
    def definir_posiciones(self, posiciones_necesarias: int) -> list:

        posiciones = Posicion.query.filter(
            Posicion.bodega == self.producto_template['bodega'],
            (Posicion.productos == '') | (Posicion.productos == '[]')
        ).limit(posiciones_necesarias).all()

        print(posiciones)

        if len(posiciones) == posiciones_necesarias:
            posiciones = [
                {
                    'id': posicion.id,
                    'nombre_posicion': posicion.nombre_posicion,
                    'volumen': posicion.volumen
                } for posicion in posiciones
            ]
            return posiciones
        else:
            return False

    def crear_producto(self, id_bodega: str, posicion: dict) -> Inventario:

        id_producto = self.crear_uuid()

        nuevo_producto = Inventario(
            id = id_producto,
            nombre = self.producto_template['nombre'],
            valorUnitario = self.producto_template['valorUnitario'],
            bodega = self.producto_template['bodega'],
            id_bodega = id_bodega,
            posicion = posicion['nombre_posicion'],
            id_posicion = posicion['id'],
            lote = self.producto_template['lote'],
            cantidadDisponible = self.producto_template['cantidad'],
            fechaIgreso = datetime.now(),
            sku = self.producto_template['sku'],
            volumen = self.producto_template['volumen']
        )
        
        db.session.add(nuevo_producto)

        return nuevo_producto

    def crear_producto_multiples_posiciones(self, id_bodega: str, posiciones: list, cantidad: int, volumen_producto: float) -> list:
        # volumen_producto = float(self.producto_template['volumen'])  # Volumen de un producto
        nuevos_productos = []  # Lista para almacenar los productos creados

        for posicion in posiciones:
            volumen_disponible = posicion['volumen']  # Volumen disponible en la posición
            capacidad_por_posicion = int(volumen_disponible // volumen_producto)  # Productos que caben en esta posición

            if capacidad_por_posicion > 0:
                # Determinar cuántos productos asignar a esta posición
                productos_a_asignar = min(capacidad_por_posicion, cantidad)

                # Crear un nuevo registro en Inventario para esta posición
                nuevo_producto = Inventario(
                    id=self.crear_uuid(),
                    nombre=self.producto_template['nombre'],
                    valorUnitario=self.producto_template['valorUnitario'],
                    bodega=self.producto_template['bodega'],
                    id_bodega=id_bodega,
                    posicion=posicion['nombre_posicion'],
                    id_posicion=posicion['id'],
                    lote=self.producto_template['lote'],
                    cantidadDisponible=productos_a_asignar,
                    fechaIgreso=datetime.now(),
                    sku=self.producto_template['sku'],
                    volumen=self.producto_template['volumen']
                )

                nuevos_productos.append(nuevo_producto)  # Agregar el producto a la lista
                cantidad -= productos_a_asignar  # Reducir la cantidad restante

            # Si ya no quedan productos por asignar, salir del bucle
            if cantidad <= 0:
                break

        # Agregar los productos creados a la sesión de la base de datos
        db.session.add_all(nuevos_productos)
        return nuevos_productos

    def agregar_stock(self, id_bodega: str, posiciones: list, cantidad: int, volumen_producto: float) -> list:

        if len(posiciones) == 1:
            try:
                nuevo_producto = self.crear_producto(id_bodega, posiciones[0])

                return [nuevo_producto]
            except Exception as e:
                print(e)
                return False
        else:
            try:
                nuevos_productos = self.crear_producto_multiples_posiciones(id_bodega, posiciones, cantidad, volumen_producto)
                return nuevos_productos
            except Exception as e:
                print(e)
                False

    def agregar_producto_a_posiciones(self, productos: list, posiciones: list):

        for i in posiciones:
            posicion = Posicion.query.filter(Posicion.id == i['id']).first()

            if not posicion.productos:
                posicion.productos = {}
            
            for i in productos:
                posicion.productos = str({"id_producto": i.id,
                                        "nombre_producto": i.nombre,
                                        "cantidad_disponible": i.cantidadDisponible,
                                        "sku": i.sku,
                                        "lote": i.lote,
                                        "volumen": i.volumen})
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
        
        if self.verificar_producto_existe():
            return {
                "response": {
                    "msg": "El producto ya existe."
                },
                "status_code": 409
            }
        
        #Obtener id de bodega
        id_bodega = self.obtener_id_bodega()
        
        # Definir numero de posiciones
        posiciones_necesarias = self.posiciones_necesarias()
        print(f'posiciones necesarias: {posiciones_necesarias}')
        
        # # Definir posiciones
        posiciones_producto = self.definir_posiciones(posiciones_necesarias)
        print(f'posiciones para el producto: {posiciones_producto}')

        if not posiciones_producto:
            return {
                "response": {
                    "msg": "No hay posiciones disponibles."
                },
                "status_code": 404
            }
        
        agregar_stock = self.agregar_stock(id_bodega, 
                                           posiciones_producto, 
                                           int(self.producto_template['cantidad']),
                                           float(self.producto_template['volumen'])
                                           )
        
        if not agregar_stock:
            return {
                "response": {
                    "msg": "Error al agregar el stock."
                },
                "status_code": 500
            }
        
        try:
            self.agregar_producto_a_posiciones(agregar_stock, posiciones_producto)
        except Exception as e:
            print(e)
            return {
                "response": {
                    "msg": f"Error al agregar el producto a la posicion",
                },
                "status_code": 500
            }
        
        try:
            
            db.session.commit()

            return {
                "response": {
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
