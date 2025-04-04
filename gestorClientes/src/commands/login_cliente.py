from werkzeug.security import check_password_hash

from src.commands.base_command import BaseCommand
from src.models.model import Cliente

class LoginCliente(BaseCommand):

    def __init__(self, request_body: dict):
        self.body = request_body
        
    def check_campos_requeridos(self) -> bool:
        required_fields = [
            "correo",
            "contrasena"
        ]

        if not all(field in self.body for field in required_fields):
            return False

        if not all(self.body.get(field) for field in required_fields):
            return False

        return True
    
    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Correo y contraseña son requeridos"
                },
                "status_code": 400
            }
        
        try:
            # Find client by email
            cliente = Cliente.query.filter_by(correo=self.body['correo']).first()
            
            # Check if client exists and password matches
            if cliente and cliente.contrasena and check_password_hash(cliente.contrasena, self.body['contrasena']):
                return {
                    "response": {
                        "msg": "Login exitoso",
                        "id": cliente.id
                    },
                    "status_code": 200
                }
            else:
                return {
                    "response": {
                        "msg": "Credenciales inválidas"
                    },
                    "status_code": 401
                }
                
        except Exception as e:
            print(e)
            return {
                "response": {
                    "msg": f"Error en el proceso de login: {str(e)}"
                },
                "status_code": 500
            } 
