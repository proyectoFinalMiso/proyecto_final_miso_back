from requests.exceptions import RequestException

from src.adapters.base_http_adapter import BaseHttpAdapter

class AdaptadorProductos(BaseHttpAdapter):
    
    def comprobar_estado_servicio(self):
        url = f"{self.url}/ping"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return True
        except RequestException:
            return False
    
    def confirmar_producto_existe(self, sku:str=None):
        url = f"{self.url}/buscar_producto"
        data = {'clave': sku}
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            producto = response.json()['body'][0]
            return producto
        except RequestException:
            return False
    
    def listar_productos(self):
        url = f"{self.url}/listar_productos"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()['body']
        except RequestException:
            return False
    
    
