import pytest
from src.models.model import db, Fabricante
from src.commands.crear_producto_masivo import CrearProductoMasivo
from src.commands.procesar_archivo_productos import ProcesarArchivoProductos
from src.commands.base_command import BaseCommand

class TestCrearProductoMasivo():
    
    def test_base_model_inherit(self):
        # Test to ensure RouteCreation inherits from BaseCommand
        productos = []
        route = CrearProductoMasivo(productos)
        assert isinstance(route, BaseCommand)

    @pytest.mark.parametrize("archivo,nombre_archivo", [
        ("tests/csv_file_product_mock.csv","csv_file_product_mock.csv"),
        ("tests/json_file_product_mock.json","json_file_product_mock.json"),
        ("tests/excel_file_product_mock.xlsx","excel_file_product_mock.xlsx")
    ])
    def test_crear_producto_masivo(self, archivo, nombre_archivo):
        db.session.query(Fabricante).delete()
        db.session.commit()

        nuevo_fabricante = Fabricante(
            id='04dab5dd-e7ab-4221-9257-03a3596aa38f',
            nombre='Teterest1',
            pais='Colombia'
        )

        nuevo_fabricante2 = Fabricante(
            id='70a99a3e-53e2-4bfd-a3d9-4181ab06dca6',
            nombre='Tesrtet2',
            pais='Colombia'
        )

        db.session.add(nuevo_fabricante)
        db.session.add(nuevo_fabricante2)
        db.session.commit()

        # Test to ensure the route creation works
        productos = ProcesarArchivoProductos(archivo, nombre_archivo).execute()
        r = CrearProductoMasivo(productos).execute()
        print(r)

        assert r['status_code'] == 201
        assert r['response']['msg'] == "Productos cargados exitosamente"
        assert r['response']['creados'] > 0