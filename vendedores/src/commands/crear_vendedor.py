import re
from uuid import uuid4
from werkzeug.security import generate_password_hash

from src.commands.base_command import BaseCommand
from src.models.model import db, Vendedor

class CrearVendedor(BaseCommand):

    def __init__(self, request_body: dict):
        self.vendedor_template = request_body

    def crear_uuid(self) -> str:
        return str(uuid4())
    
    def check_campos_requeridos(self) -> bool:

        if self.vendedor_template.get('nombre') and self.vendedor_template.get('email') and self.vendedor_template.get('contrasena'):
            return True
        else:
            return False
        
    def verificar_vendedor_existe(self) -> bool:
        
        existe_vendedor_query = Vendedor.query.filter(
            Vendedor.email == self.vendedor_template['email']
        ).first()

        if existe_vendedor_query:
            return True
        else:
            return False
        
    def verificar_email_valido(self) -> bool:
        
        patron_email = r'^[\w\.-]+@ccp.com'

        if re.match(patron_email, self.vendedor_template['email']):
            return True
        else:
            return False
        
    def execute(self):

        if not self.check_campos_requeridos():
            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }
        
        if self.verificar_vendedor_existe():
            return {
                "response": {
                    "msg": "Vendedor ya existe"
                },
                "status_code": 409
            }
        
        if not self.verificar_email_valido():
            return {
                "response": {
                    "msg": "Email invalido"
                },
                "status_code": 400
            }
        
        id_vendedor = self.crear_uuid()

        hashed_password = generate_password_hash(self.vendedor_template['contrasena'])

        nuevo_vendedor = Vendedor(
            id=id_vendedor,
            nombre=self.vendedor_template['nombre'],
            email=self.vendedor_template['email'],
            contrasena=hashed_password
        )

        db.session.add(nuevo_vendedor)

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Vendedor creado con exito"
                },
                "status_code": 201
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al crear vendedor"
                },
                "status_code": 500
            }
        


