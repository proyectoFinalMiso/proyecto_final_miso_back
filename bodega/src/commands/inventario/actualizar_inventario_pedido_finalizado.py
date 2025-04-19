from src.models.model import db, Inventario, NecesidadCompras


class InventarioPedidoFinalizado:
    """
    Esta función se encarga de reservar el inventario disponible en el inventario. Calcula la reserva y la necesidad por producto
    y se encarga de restar el producto retirado del lote más viejo. Para este caso, se hace la suposición de que un producto no
    está en múltiples bodegas
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

    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {"msg": "Campos requeridos no cumplidos"},
                "status_code": 400,
            }

        for producto_reservado in self.body:
            sku = producto_reservado["sku"]
            retirar_reserva = producto_reservado["cantidad"]

            lotes_inventario = (
                db.session.query(Inventario)
                .filter(Inventario.sku == sku)
                .order_by(Inventario.fechaIgreso.asc())
                .all()
            )
            registro_necesidad = (
                db.session.query(NecesidadCompras)
                .filter(NecesidadCompras.sku == sku)
                .first()
            )

            if registro_necesidad:
                if registro_necesidad.cantidad <= 0:
                    for lote in lotes_inventario:
                        if lote.cantidadReservada > 0:
                            cantidad_a_recuperar = min(
                                retirar_reserva, lote.cantidadReservada
                            )
                            lote.cantidadReservada -= cantidad_a_recuperar
                            retirar_reserva -= cantidad_a_recuperar
            else:
                for lote in lotes_inventario:
                    if lote.cantidadReservada > 0:
                        cantidad_a_recuperar = min(
                            retirar_reserva, lote.cantidadReservada
                        )
                        lote.cantidadReservada -= cantidad_a_recuperar
                        retirar_reserva -= cantidad_a_recuperar

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Se ha actualizado la reserva de productos en el sistema por la finalización de un pedido", 
                    "body": str(self.body)
                },
                "status_code": 201,
            }

        except Exception as e:
            db.session.rollback()
            return {
                "response": {
                    "msg": f"Ha ocurrido un error al actualizar el inventario: {e}"
                },
                "status_code": 500,
            }
