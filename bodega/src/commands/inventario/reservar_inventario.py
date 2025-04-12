from sqlalchemy.sql import func
from src.models.model import db, Inventario, NecesidadCompras


class ReservarInventario:
    """
    Esta función se encarga de reservar el inventario disponible en el inventario cuándo se crea un nuevo pedido en la plataforma. 
    La lógica es primero reservar los lotes por orden de antiguedad. En caso de que la necesidad sea superior a la cantidad disponible, 
    se almacena en una tabla secundaria para la visualización del equipo de compras
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
        lista_reserva = []
        for producto in self.body:
            existencias = (
                db.session.query(func.sum(Inventario.cantidadDisponible))
                .filter(Inventario.sku == producto["sku"])
                .scalar() or 0
            )
            solicitado = producto['cantidad']
            reserva = min(existencias, solicitado)
            necesidad = 0
            if reserva < solicitado:
                necesidad = solicitado - reserva
            lista_reserva.append(
                {
                    "sku": producto["sku"],
                    "reserva": reserva,
                    "necesidad": necesidad,
                }
            )
        return lista_reserva

    def execute(self):        
        if not self.check_campos_requeridos():
            return {
                "response": {"msg": "Campos requeridos no cumplidos"},
                "status_code": 400,
            }
        
        lista_reserva = self.calcular_reserva_y_necesidad()
        
        for producto_reservado in lista_reserva:
            sku = producto_reservado['sku']
            reserva = producto_reservado['reserva']
            necesidad = producto_reservado['necesidad']

            lotes_inventario = db.session.query(Inventario).filter(
                Inventario.sku == sku,
                Inventario.cantidadDisponible > 0).order_by(Inventario.fechaIgreso.asc()).all()
            
            for lote in lotes_inventario:
                if reserva <= 0:
                    break
                if lote.cantidadDisponible > 0:
                    cantidad_a_reservar = min(reserva, lote.cantidadDisponible)
                    lote.cantidadDisponible -= cantidad_a_reservar
                    lote.cantidadReservada += cantidad_a_reservar
                    reserva -= cantidad_a_reservar

            if necesidad > 0:
                registro_necesidad = db.session.query(NecesidadCompras).filter(
                    NecesidadCompras.sku == sku).first()
                
                if not registro_necesidad:
                    registro_necesidad = NecesidadCompras(sku=sku, cantidad=necesidad)
                    db.session.add(registro_necesidad)
                else:
                    registro_necesidad.cantidad += necesidad
            
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
                

