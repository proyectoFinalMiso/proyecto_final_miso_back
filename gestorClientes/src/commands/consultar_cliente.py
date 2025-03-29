from src.commands.base_command import BaseCommand
from src.models.model import db, Cliente

class ConsultarCliente(BaseCommand):

    def __init__(self, cliente_id: str):
        self.cliente_id = cliente_id

    def check_campos_requeridos(self) -> bool:
        if self.cliente_id:
            return True
        else:
            return False
    
    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "El ID del cliente es requerido"
                },
                "status_code": 400
            }
        
        try:
            cliente = Cliente.query.filter_by(id=self.cliente_id).first()
            
            if not cliente:
                return {
                    "response": {
                        "msg": "Cliente no encontrado"
                    },
                    "status_code": 404
                }
            
            cliente_data = {
                "id": cliente.id,
                "nombre": cliente.nombre,
                "correo": cliente.correo,
                "vendedorAsociado": cliente.vendedorAsociado
            }
            
            return {
                "response": {
                    "cliente": cliente_data
                },
                "status_code": 200
            }
        except Exception as e:
            print(e)
            return {
                "response": {
                    "msg": "Error al consultar cliente"
                },
                "status_code": 500
            } 
