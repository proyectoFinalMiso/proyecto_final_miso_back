from src.commands.base_command import BaseCommand
from src.models.model import db, PlanVentas

class ListarPlanes(BaseCommand):
    def buscar_planes(self) -> list:
        planes = PlanVentas.query.all()
        if not planes:
            return False
        return [
            {
                "id": plan.id,
                "vendedor_id": plan.vendedor_id,
                "vendedor_nombre": plan.vendedor_nombre,
                "estado": plan.estado.value,
                "fecha_inicio": plan.fecha_inicio,
                "fecha_final": plan.fecha_final,
                "meta_ventas": plan.meta_ventas,
                "productos_plan": plan.productos_plan,
            }
            for plan in planes
        ]
    
    def execute(self):
        try:
            planes = self.buscar_planes()
            if not planes:
                return {
                    "response": {
                        "msg": "No hay planes disponibles",
                    },
                    "status_code": 404,
                }
            return {
                "response": {
                    "msg": "Lista de planes",
                    "body": planes,
                },
                "status_code": 200,
            }
            
        except Exception as e:
            return {
                "response": {
                    "msg": "Problemas con la conexión a la base de datos.",
                    "error": str(e),
                },
                "status_code": 500,
            }