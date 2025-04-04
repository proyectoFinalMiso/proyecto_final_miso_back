from uuid import uuid4, UUID
from werkzeug.security import generate_password_hash

from src.commands.base_command import BaseCommand
from src.models.model import db, Cliente

class CrearCliente(BaseCommand):

    def __init__(self, request_body: dict):
        self.body = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def verificar_cliente_existe(self) -> bool:
        existe_cliente_query = Cliente.query.filter(
            (Cliente.nombre == self.body['nombre']) &
            (Cliente.correo == self.body['correo'])
        ).first()

        if existe_cliente_query:
            return True
        else:
            return False
        
    def verificar_id_existe(self, id: UUID) -> bool:
        existe_id_query = Cliente.query.filter(
            (Cliente.id == id)
        ).first()

        if existe_id_query:
            return True
        else:
            return False
        
    def check_campos_requeridos(self) -> bool:
        required_fields = [
            "nombre",
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
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
        
        if self.verificar_cliente_existe():
            return {
                "response": {
                    "msg": "Cliente ya existe"
                },
                "status_code": 400
            }
        
        
        
        id_cliente_unico = False
        while not id_cliente_unico:
            id_cliente = self.crear_uuid()
            if not self.verificar_id_existe(id_cliente):
                id_cliente_unico = True

        # Hash the password
        hashed_password = generate_password_hash(self.body['contrasena'])

        nuevo_cliente = Cliente(
            id=id_cliente,
            nombre=self.body['nombre'],
            correo=self.body['correo'],
            contrasena=hashed_password
        )
        
        if 'vendedorAsociado' in self.body and self.body['vendedorAsociado']:
            nuevo_cliente.vendedorAsociado = self.body['vendedorAsociado']
            
        db.session.add(nuevo_cliente)

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Cliente creado con éxito",
                    "id": id_cliente
                },
                "status_code": 201
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "response": {
                    "msg": f"Error al crear cliente: {str(e)}"
                },
                "status_code": 500
            } 
