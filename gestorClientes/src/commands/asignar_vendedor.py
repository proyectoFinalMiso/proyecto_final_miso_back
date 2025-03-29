from src.commands.base_command import BaseCommand
from src.models.model import db, Cliente

class AsignarVendedor(BaseCommand):

    def __init__(self, cliente_id: str, vendedor_id: str):
        self.cliente_id = cliente_id
        self.vendedor_id = vendedor_id
    
    def execute(self):
        try:
            cliente = Cliente.query.filter_by(id=self.cliente_id).first()
            
            if not cliente:
                return {
                    "response": {
                        "msg": "Cliente no encontrado"
                    },
                    "status_code": 404
                }
            
            cliente.vendedorAsociado = self.vendedor_id
            db.session.commit()
            
            cliente_data = {
                "id": cliente.id,
                "nombre": cliente.nombre,
                "correo": cliente.correo,
                "vendedorAsociado": cliente.vendedorAsociado
            }
            
            return {
                "response": {
                    "msg": "Vendedor asignado correctamente",
                    "cliente": cliente_data
                },
                "status_code": 200
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al asignar vendedor"
                },
                "status_code": 500
            } 
