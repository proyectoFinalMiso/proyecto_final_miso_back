from uuid import uuid4
from datetime import datetime

from src.commands.base_command import BaseCommand
from src.models.model import db, PlanVentas

class CrearPlanVentas(BaseCommand):

    def __init__(self, request_body: dict):
        self.plan_template = request_body

    def check_campos_requeridos(self) -> bool:
        
        required_fields = ['vendedor_id', 'vendedor_nombre', 'estado', 'fechaInicio', 'metaVentas', 'productosPlan']

        if not all(field in self.plan_template for field in required_fields):
            return False
        if not all(self.plan_template.get(field) for field in required_fields):
            return False
        return True
    
    def verificar_vendedor_existe(self) -> bool:
        
        existe_vendedor_query = PlanVentas.query.filter(
            PlanVentas.vendedor_id == self.plan_template['vendedor_id']
        ).first()

        if existe_vendedor_query:
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
                    "msg": "Vendedor no existe"
                },
                "status_code": 400
            }

        plan_ventas = PlanVentas(
            id=str(uuid4()),
            vendedor_id=self.plan_template['vendedor_id'],
            vendedor_nombre=self.plan_template['vendedor_nombre'],
            estado=self.plan_template['estado'],
            fechaInicio=datetime.now(),
            metaVentas=self.plan_template['metaVentas'],
            productosPlan=self.plan_template['productosPlan']
        )

        db.session.add(plan_ventas)

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Plan de ventas creado exitosamente",
                    "plan_ventas": {
                        "id": plan_ventas.id,
                        "productos": plan_ventas.productosPlan,
                        "menta": plan_ventas.metaVentas}
                },
                "status_code": 201
            }
        
        except Exception as e:
            db.session.rollback()
            print(e)
            return {
                "response": {
                    "msg": "Error al crear el plan de ventas",
                    "error": str(e)
                },
                "status_code": 500
            }