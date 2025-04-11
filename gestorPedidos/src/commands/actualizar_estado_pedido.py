from src.commands.base_command import BaseCommand
from src.models.model import Pedido, db

class ActualizarEstadoPedido(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body
    
    def check_campos_requeridos(self) -> bool:
        required_fields = [
            "id",
            "estado"
        ]

        if not all(field in self.body for field in required_fields):
            return False
        
        if not all(self.body.get(field) for field in required_fields):
            return False

        return True
    
    def check_status_integrity(self) -> bool:
        if self.body.get("estado") not in ["FINALIZADO", "CANCELADO"]:
            return False
        return True
        

    def execute(self):
        if not self.check_campos_requeridos():
            return {'response': {'msg': 'La petición no cuenta con todos los campos requeridos'}, 'status_code': 400}
        if not self.check_status_integrity():
            return {'response': {'msg': 'El estado del pedido debe ser FINALIZADO o CANCELADO'}, 'status_code': 400}
        
        pedido = Pedido.query.filter_by(id=self.body['id']).first()
        if not pedido:
            return {'response': {'msg': 'El pedido no existe'}, 'status_code': 404}
        
        pedido.estado = self.body['estado']
        try:
            db.session.add(pedido)
            db.session.commit()
            return {'response': {'msg': 'El estado del pedido se actualizó correctamente', 'body': {'id': pedido.id, 'estado': pedido.estado.value}}, 'status_code': 200}
        except Exception as e:
            db.session.rollback()
            return {'response': {'msg': f'No se ha podido completar la actualización del estado: {e}'}, 'status_code': 500}