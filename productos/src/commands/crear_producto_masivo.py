from uuid import uuid4, UUID

from src.commands.base_command import BaseCommand
from src.models.model import db, Fabricante, Producto


class CrearProductoMasivo(BaseCommand):
    def __init__(self, productos: list):
        self.productos = productos
        self.productos_a_insertar = []
        self.productos_ignorados = []

    def check_campos_requeridos(self, producto):
        return all(
            key in producto
            for key in ["nombre", "volumen", "id_fabricante", "valorUnitario"]
        )

    def verificar_fabricante_existe(self, producto) -> bool:
        return (
            db.session.query(Fabricante.id).filter_by(id=producto['id_fabricante']).scalar()
            is not None
        )

    def verificar_producto_existe(self, producto) -> bool:
        return (
            db.session.query(Producto.id)
            .filter_by(nombre=producto['nombre'], fabricante=producto['id_fabricante'])
            .scalar()
            is not None
        )

    def crear_uuid(self):
        return str(uuid4())

    def verificar_id_existe(self, id: UUID) -> bool:
        existe_id_query = Producto.query.filter((Producto.id == id)).first()

        if existe_id_query:
            return True
        else:
            return False

    def execute(self):
        for producto in self.productos:
            if not self.check_campos_requeridos(producto):
                self.productos_ignorados.append(
                    {
                        "producto": producto,
                        "causa": "El producto no cuenta con todos los campos requeridos",
                    }
                )
                continue

            if self.verificar_producto_existe(producto):
                self.productos_ignorados.append(
                    {
                        "producto": producto,
                        "causa": "El producto ya existe en el sistema",
                    }
                )
                continue

            if not self.verificar_fabricante_existe(
                producto
            ):
                self.productos_ignorados.append(
                    {
                        "producto": producto,
                        "causa": "El fabricante asociado al producto no existe",
                    }
                )
                continue

            id_unico = False
            while not id_unico:
                id_producto = self.crear_uuid()
                if not self.verificar_id_existe(id_producto):
                    id_unico = True

            nuevo_producto = Producto(
                id=id_producto,
                fabricante=producto["id_fabricante"],
                nombre=producto["nombre"],
                valorUnitario=producto["valorUnitario"],
                volumen=producto["volumen"],
            )
            self.productos_a_insertar.append(nuevo_producto)

        if self.productos_a_insertar:
            try:
                db.session.bulk_save_objects(self.productos_a_insertar)
                db.session.commit()
                return {
                    "response": {
                        "msg": "Productos cargados exitosamente",
                        "creados": len(self.productos_a_insertar),
                        "ignorados": self.productos_ignorados,
                    },
                    "status_code": 201,
                }
            except Exception as e:
                db.session.rollback()
                return {
                    "response": {"msg": f"Error al cargar productos: {str(e)}"},
                    "status_code": 500,
                }
        return {
            "response": {
                "msg": "No se ha cargado ningún producto",
                "ignorados": self.productos_ignorados,
            },
            "status_code": 400,
        }
