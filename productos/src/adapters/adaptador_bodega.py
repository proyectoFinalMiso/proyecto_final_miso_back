from requests.exceptions import RequestException

from src.adapters.base_http_adapter import BaseHttpAdapter

class AdaptadorBodega(BaseHttpAdapter):
    
    def comprobar_estado_servicio(self):
        url = f"{self.url}/ping"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return True
        except RequestException:
            return False
    
    def listar_existencias(self):
        url = f"{self.url}/inventario_total"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            existencias = response.json()['data']
            return existencias
        except RequestException:
            return False
    
    def listar_necesidad(self):
        url = f"{self.url}/inventario_necesidad"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            necesidades = response.json()['body']
            return necesidades
        except RequestException:
            return False
    
    
