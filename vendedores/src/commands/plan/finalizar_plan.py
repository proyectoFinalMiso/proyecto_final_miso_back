from src.commands.base_command import BaseCommand
from src.models.model import db, PlanVentas, EstadoPlan
from datetime import datetime

class FinalizarPlan(BaseCommand):
    def __init__(self, request_body: dict):
        self.plan_template = request_body

    def verificar_plan_existe(self) -> bool:
        existe_plan_query = PlanVentas.query.filter(
            PlanVentas.id == self.plan_template['id']
        ).first()

        if existe_plan_query:
            return True
        else:
            return False
        
    def verificar_plan_finalizado(self) -> bool:
        existe_plan_query = PlanVentas.query.filter(
            PlanVentas.id == self.plan_template['id']
        ).first()

        if existe_plan_query.estado == EstadoPlan.FINALIZADO:
            return False
        else:
            return True

    def execute(self):
        if not self.verificar_plan_existe():
            return {
                "response": {
                    "msg": "El plan no existe"
                },
                "status_code": 400
            }
        
        if not self.verificar_plan_finalizado():
            return {
                "response": {
                    "msg": "El plan ya ha sido finalizado"
                },
                "status_code": 400
            }

        plan = PlanVentas.query.filter_by(id=self.plan_template['id']).first()
        print(plan)
        plan.estado = 'FINALIZADO' #str(EstadoPlan.FINALIZADO)
        plan.fechaFinal = datetime.now()
        db.session.commit()

        return {
            "response": {
                "msg": "Plan finalizado",
                "body": {
                    "id": plan.id,
                    "estado": plan.estado.value,
                    "fechaFinal": plan.fechaFinal,
                }
            },
            "status_code": 200
        }