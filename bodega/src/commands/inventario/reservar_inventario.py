from src.models.model import db, Inventario

class ReservarInventario:
    """
    Esta función se encarga de reservar el inventario  
    """
    def __init__(self, productos: list = None):
        self.body = productos
    
    def check_campos_requeridos(self) -> bool:
        required_fields = [
            "sku",
            "cantidad"
        ]

        if not all(field in self.body for field in required_fields):
            return False

        if not all(self.body.get(field) for field in required_fields):
            return False

        return True
    
    def execute(self):
        for producto in self.body:
            if not self.check_campos_requeridos():
                return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
