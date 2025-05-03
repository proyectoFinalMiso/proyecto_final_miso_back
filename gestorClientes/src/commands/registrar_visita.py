from src.models.model import db, Cliente, Visita, EstadoVisita
from src.commands.base_command import BaseCommand
import requests
import os
from datetime import datetime

class RegistrarVisita(BaseCommand):
    def __init__(self, cliente_id, request_body: dict):
        self.cliente_id = cliente_id
        self.body = request_body

    def check_campos_requeridos(self) -> bool:
        required_fields = [
            "vendedor_id",
            "fecha",
            "estado"
        ]

        if not all(field in self.body for field in required_fields):
            return False

        if not all(self.body.get(field) for field in required_fields):
            return False

        return True
    
    def verificar_vendedor_existe(self):
        vendedores_api = os.getenv("MS_VENDEDOR_URL")
        url = f"{vendedores_api}/obtener_vendedor/{self.body['vendedor_id']}"
        
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error al verificar vendedor: {e}")
            return False
        
    def validate_date_format(self, date_string):
        try:
            date_obj = datetime.fromisoformat(date_string)
            return date_obj
        except (ValueError, TypeError):
            return None
        
    def execute(self):
        try:
            if not self.check_campos_requeridos():
                return {
                    "response": {
                        "msg": "El ID del cliente, ID del vendedor y la fecha son requeridos"
                    },
                    "status_code": 400
                }
            
            date_obj = self.validate_date_format(self.body["fecha"])
            if not date_obj:
                return {
                    "response": {
                        "msg": "Formato de fecha inválido. Debe ser ISO format (YYYY-MM-DDTHH:MM:SS)"
                    },
                    "status_code": 400
                }
                
            self.body["fecha"] = date_obj

            estado = self.body.get("estado")
            try:
                self.body["estado"] = EstadoVisita(estado)
            except ValueError:
                return {
                    "response": {
                        "msg": "Estado de visita inválido"
                    },
                    "status_code": 400
                }
            
            if self.body["estado"] == EstadoVisita.PROGRAMADA and date_obj < datetime.now():
                return {
                    "response": {
                        "msg": "No se puede registrar una visita programada en el pasado"
                    },
                    "status_code": 400
                }

            visita_existente = Visita.query.filter_by(
                cliente_id=self.cliente_id,
                vendedor_id=self.body["vendedor_id"],
                fecha=date_obj
            ).first()
            if visita_existente:
                return {
                    "response": {
                        "msg": "Ya existe una visita registrada para este cliente, vendedor y fecha"
                    },
                    "status_code": 400
                }
            
            if not self.verificar_vendedor_existe():
                return {
                    "response": {
                        "msg": "Vendedor no encontrado"
                    },
                    "status_code": 404
                }
            
            cliente = Cliente.query.filter_by(id=self.cliente_id).first()
            
            if not cliente:
                return {
                    "response": {
                        "msg": "Cliente no encontrado"
                    },
                    "status_code": 404
                }
            
            visita = Visita(
                cliente_id=self.cliente_id,
                vendedor_id=self.body["vendedor_id"],
                fecha=self.body["fecha"],
                estado=self.body["estado"]
            )

            db.session.add(visita)
            db.session.commit()

            visita_data = {
                "id": visita.id,
                "cliente_id": visita.cliente_id,
                "vendedor_id": visita.vendedor_id,
                "fecha": visita.fecha.isoformat(),
                "estado": visita.estado.value
            }

            return {
                "response": {
                    "msg": "Visita registrada correctamente",
                    "visita": visita_data
                },
                "status_code": 200
            }
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "response": {
                    "msg": "Error al registrar visita"
                },
                "status_code": 500
            }
