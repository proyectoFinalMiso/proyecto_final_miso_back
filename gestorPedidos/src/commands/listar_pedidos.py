from src.commands.base_command import BaseCommand
from src.models.model import Pedido


class ListarPedidos(BaseCommand):

    def __init__(self, cliente_id: str = None):
        self.cliente_id = cliente_id

    def execute(self):
        try:
            if self.cliente_id:
                pedidos = Pedido.query.filter_by(cliente=self.cliente_id).all()
            else:
                pedidos = Pedido.query.all()

            pedidos_list = []
            for pedido in pedidos:
                pedidos_list.append(
                    {
                        "id": pedido.id,
                        "cliente": pedido.cliente,
                        "vendedor": pedido.vendedor,
                        "packingList": pedido.packingList,
                        "fechaIngreso": pedido.fechaIngreso,
                        "direccion": pedido.direccion,
                        "latitud": pedido.latitud,
                        "longitud": pedido.longitud,
                        "estado": pedido.estado.value,
                        "valorFactura": pedido.valorFactura,
                    }
                )

            return {"response": {"pedidos": pedidos_list}, "status_code": 200}

        except Exception as e:
            return {
                "response": {"msg": f"Error al listar los pedidos: {e}"},
                "status_code": 500,
            }
