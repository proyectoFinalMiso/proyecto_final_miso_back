from src.commands.base_command import BaseCommand
from src.models.model import db, Cliente

class ListarClientes(BaseCommand):
    
    def execute(self):
        try:
            clientes = Cliente.query.all()
            
            clientes_list = []
            for cliente in clientes:
                clientes_list.append({
                    "id": cliente.id,
                    "nombre": cliente.nombre,
                    "correo": cliente.correo,
                    "vendedorAsociado": cliente.vendedorAsociado
                })
            
            return {
                "response": {
                    "clientes": clientes_list
                },
                "status_code": 200
            }
        except Exception as e:
            print(e)
            return {
                "response": {
                    "msg": "Error al listar clientes"
                },
                "status_code": 500
            } 
