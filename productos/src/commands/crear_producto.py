from uuid import uuid4, UUID

from src.commands.base_command import BaseCommand
from src.models.model import db, Fabricante, Producto


class CrearProducto(BaseCommand):
    def __init__(self, request_body: dict):
        self.producto_template = request_body

    def verificar_producto_existe(self) -> bool:
        existe_producto_query = Producto.query.filter(
            (Producto.nombre == self.producto_template["nombre"]) &
            (Producto.fabricante == self.producto_template["id_fabricante"])
        ).first()

        if existe_producto_query:
            return True
        else:
            return False
    
    def verificar_fabricante_existe(self, id_fabricante) -> bool:
        existe_fabricante_query = Fabricante.query.filter(
            (Fabricante.id == id_fabricante)
        ).first()

        if existe_fabricante_query:
            return True
        else:
            return False
    
    def verificar_id_existe(self, id: UUID) -> bool:
        existe_id_query = Producto.query.filter(
            (Producto.id == id)
        ).first()

        if existe_id_query:
            return True
        else:
            return False

    def crear_uuid(self) -> str:
        return str(uuid4())

    def check_campos_requeridos(self) -> bool:
        if (
            self.producto_template.get("id_fabricante")
            and self.producto_template.get("nombre")
            and self.producto_template.get("valorUnitario")
        ):
            return True
        else:
            return False

    def execute(self):
        if not self.check_campos_requeridos():
            return {
                "response": {"msg": "Campos requeridos no cumplidos"},
                "status_code": 400,
            }

        if self.verificar_producto_existe():
            return {"response": {"msg": "Producto ya existe"}, "status_code": 400}
        
        if not self.verificar_fabricante_existe(self.producto_template["id_fabricante"]):
            return {"response": {"msg": "El fabricante indicado no existe"}, "status_code": 400}

        id_unico = False
        while not id_unico:
            id_producto = self.crear_uuid()
            if not self.verificar_id_existe(id_producto):
                id_unico = True

        nuevo_producto = Producto(
            id=id_producto,        
            fabricante=self.producto_template["id_fabricante"],
            nombre=self.producto_template["nombre"],
            valorUnitario=self.producto_template["valorUnitario"],
        )

        db.session.add(nuevo_producto)

        try:
            db.session.commit()
            return {
                "response": {"msg": "Producto creado exitosamente"},
                "status_code": 201,
            }
        except Exception as e:
            db.session.rollback()
            return {
                "response": {"msg": f"Error al crear un nuevo producto: {str(e)}"},
                "status_code": 500,
            }
