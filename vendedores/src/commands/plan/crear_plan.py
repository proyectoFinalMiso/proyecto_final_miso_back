from uuid import uuid4
from datetime import datetime

from src.commands.base_command import BaseCommand
from src.models.model import db, PlanVentas, Vendedor

class CrearPlanVentas(BaseCommand):

    def __init__(self, request_body: dict):
        self.plan_template = request_body

    def check_campos_requeridos(self) -> bool:
        
        required_fields = ['vendedor_id', 'vendedor_nombre', 'meta_ventas', 'productos_plan']

        if not all(field in self.plan_template for field in required_fields):
            return False
        if not all(self.plan_template.get(field) for field in required_fields):
            return False
        return True
    
    def verificar_vendedor_existe(self) -> bool:
        
        existe_vendedor_query = Vendedor.query.filter(
            Vendedor.id == self.plan_template['vendedor_id']
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

        if not self.verificar_vendedor_existe():
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
            estado='INICIADO',
            fecha_inicio=datetime.now(),
            meta_ventas=self.plan_template['meta_ventas'],
            productos_plan=self.plan_template['productos_plan']
        )

        db.session.add(plan_ventas)

        try:
            db.session.commit()
            return {
                "response": {
                    "msg": "Plan de ventas creado exitosamente",
                    "plan_ventas": {
                        "id": plan_ventas.id,
                        "productos": plan_ventas.productos_plan,
                        "menta": plan_ventas.meta_ventas}
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