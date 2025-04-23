import requests
from src.constants.urls import CLIENT_URL, SELLER_URL
from src.commands.base_command import BaseCommand
from src.models.model import Pedido


class ListarPedidos(BaseCommand):

    def __init__(self, cliente_id: str = None):
        self.cliente_id = cliente_id
        
    def _get_json_from_url(self, url: str, key: str):
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code not in [200, 201]:
                raise Exception(f"Error {response.status_code}: {response.text}")
            return response.json().get(key, [])
        except requests.RequestException as e:
            raise Exception(f"Error de conexión al hacer GET a {url}: {str(e)}")

    def obtener_clientes(self):
        return self._get_json_from_url(CLIENT_URL + "/clientes", "clientes")

    def obtener_vendedores(self):
        return self._get_json_from_url(SELLER_URL + "/listar_vendedores", "body")
    
    def encontrar_por_id(self, elementos: list, id: str):
        return next((elemento for elemento in elementos if elemento["id"] == id), None)

    def execute(self):
        try:
            if self.cliente_id:
                pedidos = Pedido.query.filter_by(cliente=self.cliente_id).all()
            else:
                pedidos = Pedido.query.all()
            
            clientes = self.obtener_clientes()
            
            vendedores = self.obtener_vendedores()
            
            pedidos_list = []
            
            for pedido in pedidos:
                
                cliente = self.encontrar_por_id(clientes, pedido.cliente)
                
                vendedor = self.encontrar_por_id(vendedores, pedido.vendedor)
                
                pedidos_list.append(
                    {
                        "id": pedido.id,
                        "cliente": cliente,
                        "vendedor": vendedor,
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
