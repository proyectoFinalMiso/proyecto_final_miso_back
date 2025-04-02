from src.commands.base_command import BaseCommand
from src.models.model import Fabricante


class ListarFabricantes(BaseCommand):
    def buscar_fabricantes(self) -> bool:
        return Fabricante.query.all()

    def execute(self):
        fabricantes = self.buscar_fabricantes()

        if not fabricantes:
            return {
                "response": {"msg": "No se han encontrado fabricantes registrados en la plataforma"},
                "status_code": 404,
            }
        return {
            "response": {"msg": "Lista de fabricantes", "body": fabricantes},
            "status_code": 200,
        }