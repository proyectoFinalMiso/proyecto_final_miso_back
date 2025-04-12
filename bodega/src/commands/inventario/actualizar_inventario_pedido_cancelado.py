from sqlalchemy.sql import func
from src.models.model import db, Inventario, NecesidadCompras


class InventarioPedidoCancelado:
    """
    Esta función se encarga de reservar el inventario disponible en el inventario. Calcula la reserva y la necesidad por producto
    y se encarga de generar la devolución del producto al inventario disponible. Siempre se resta primero la necesidad al SKU,
    luego se resta la reserva en orden ascendente de fecha de ingreso. Finalmente, la cantidad recuperada se agrega al lote más
    nuevo con reserva asociada
    """

    def __init__(self, productos: list = None):
        self.body = productos

    def check_campos_requeridos(self) -> bool:
        check = True
        for producto in self.body:
            required_fields = ["sku", "cantidad"]
            if not all(field in producto for field in required_fields):
                check = False

            if not all(producto.get(field) for field in required_fields):
                check = False

        return check

    def calcular_reserva_y_necesidad(self) -> list:
        lista_cantidades = []
        for producto in self.body:
            cantidad_retirar_necesidad = 0
            cantidad_retirar_reserva = 0
            cantidad_agregar_inventario = 0

            cantidad_reingresar = producto['cantidad']
            cantidad_reservada = (
                db.session.query(func.sum(Inventario.cantidadReservada))
                .filter(Inventario.sku == producto["sku"])
                .scalar() or 0
            )
            cantidad_necesidad = (
                db.session.query(func.sum(NecesidadCompras.cantidad))
                .filter(NecesidadCompras.sku == producto["sku"])
                .scalar() or 0
            )

            # Iniciar restando la necesidad
            cantidad_retirar_necesidad = min(cantidad_necesidad, cantidad_reingresar)
            if cantidad_retirar_necesidad < cantidad_reingresar:
                residual_retiro_necesidad = cantidad_reingresar - cantidad_retirar_necesidad
                cantidad_retirar_reserva = min(cantidad_reingresar - cantidad_retirar_necesidad, cantidad_reservada)
                if cantidad_retirar_reserva < residual_retiro_necesidad:
                    cantidad_agregar_inventario = residual_retiro_necesidad - cantidad_retirar_reserva
            lista_cantidades = {
                'sku': producto['sku'],
                'retirar_necesidad': cantidad_retirar_necesidad,
                'retirar_reserva': cantidad_retirar_reserva,
                'agregar_inventario': cantidad_agregar_inventario
            }

        return lista_cantidades
                
                
    def execute(self):        
        if not self.check_campos_requeridos():
            return {
                "response": {"msg": "Campos requeridos no cumplidos"},
                "status_code": 400,
            }
        
        lista_reserva = self.calcular_reserva_y_necesidad()
        
        for producto_reservado in lista_reserva:
            sku = producto_reservado['sku']
            retirar_necesidad = producto_reservado['retirar_necesidad']
            retirar_reserva = producto_reservado['retirar_reserva']
            agregar_inventario = producto_reservado['agregar_inventario']

            lotes_inventario = db.session.query(Inventario).filter(
                Inventario.sku == sku,
                Inventario.cantidadDisponible > 0).order_by(Inventario.fechaIgreso.asc()).all()
            
            if retirar_necesidad > 0:
                registro_necesidad = db.session.query(NecesidadCompras).filter(
                    NecesidadCompras.sku == sku).first()
                registro_necesidad.cantidad -= retirar_necesidad
            
            for lote in lotes_inventario:
                if retirar_reserva + agregar_inventario <= 0:
                    break

                if lote.cantidadReservada > 0:
                    cantidad_a_recuperar = min(retirar_reserva, lote.cantidadReservada)
                    lote.cantidadReservada -= cantidad_a_recuperar
                    retirar_reserva -= cantidad_a_recuperar
                    if cantidad_a_recuperar == 0:
                        lote.cantidadDisponible += agregar_inventario
                        agregar_inventario = 0                    
            
        try:
            db.session.commit()
            return {
                "response": {
                    "msg": f"Se ha actualizado la reserva de productos en el sistema: {lista_reserva}"
                },
                "status_code": 200
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": f"Ha ocurrido un error al actualizar el inventario: {e}"
                },
                "status_code": 500
            }
                

