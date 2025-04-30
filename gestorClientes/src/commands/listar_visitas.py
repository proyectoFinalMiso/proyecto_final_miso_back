from src.commands.base_command import BaseCommand
from src.models.model import db, Visita, EstadoVisita

class ListarVisitas(BaseCommand):
    def __init__(self, cliente_id=None, vendedor_id=None, estado=None, sort_order=None):
        self.cliente_id = cliente_id
        self.vendedor_id = vendedor_id
        self.estado = None
        if estado is not None:
            try:
                self.estado = EstadoVisita(estado)
            except ValueError:
                self.estado = None
        self.sort_order = sort_order if sort_order is not None else 'asc'
        
        if self.sort_order not in ['asc', 'desc']:
            self.sort_order = 'asc'

    def execute(self):
        try:
            query = Visita.query
            
            if self.cliente_id:
                query = query.filter_by(cliente_id=self.cliente_id)
                
            if self.vendedor_id:
                query = query.filter_by(vendedor_id=self.vendedor_id)
                
            if self.estado is not None:
                query = query.filter_by(estado=self.estado)
            
            if str(self.sort_order).lower() == 'desc':
                query = query.order_by(Visita.fecha.desc())
            else:
                query = query.order_by(Visita.fecha.asc())
                
            visitas = query.all()

            if not visitas:
                return {
                    "response": {
                        "msg": "No se encontraron visitas con los criterios especificados"
                    },
                    "status_code": 404
                }

            visitas_data = [
                {
                    "id": visita.id,
                    "cliente_id": visita.cliente_id,
                    "vendedor_id": visita.vendedor_id,
                    "estado": visita.estado.value,
                    "fecha": visita.fecha.isoformat()
                } for visita in visitas
            ]

            return {
                "response": {
                    "visitas": visitas_data
                },
                "status_code": 200
            }
        except Exception as e:
            return {
                "response": {
                    "msg": str(e)
                },
                "status_code": 500
            }
