import pytest
import os
from src.commands.procesar_archivo_productos import ProcesarArchivoProductos
from src.commands.base_command import BaseCommand

class TestProcesarArchivoProductos():
    DATA_DIR = os.path.dirname(__file__)

    @pytest.mark.parametrize("archivo,nombre_archivo", [
        ("tests/csv_file_product_mock.csv","csv_file_product_mock.csv"),
        ("tests/json_file_product_mock.json","json_file_product_mock.json"),
        ("tests/excel_file_product_mock.xlsx","xlsx_file_product_mock.xlsx")
    ])    
    def test_base_model_inherit(self, archivo, nombre_archivo):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = ProcesarArchivoProductos(archivo, nombre_archivo)
        assert isinstance(route, BaseCommand)
    
    @pytest.mark.parametrize("archivo,nombre_archivo", [
        ("tests/csv_file_product_mock.csv","csv_file_product_mock.csv"),
        ("tests/json_file_product_mock.json","json_file_product_mock.json"),
        ("tests/excel_file_product_mock.xlsx","xlsx_file_product_mock.xlsx")
    ])    
    def test_procesar_archivo_es_valido(self, archivo, nombre_archivo):
        with open(archivo, "rb") as f:
            procesador = ProcesarArchivoProductos(f, nombre_archivo)
            response = procesador.execute()
            assert response['status_code'] == 200
            resultado = response['response']['payload']
            assert isinstance(resultado, list)
            assert len(resultado) > 0
            for producto in resultado:
                assert "nombre" in producto
                assert "valorUnitario" in producto
                assert "volumen" in producto
                assert "id_fabricante" in producto 
    
    @pytest.mark.parametrize("archivo,nombre_archivo", [
        ("tests/csv_file_invalid_mock.csv","csv_file_invalid_mock.csv"),
        ("tests/json_file_invalid_mock.json","json_file_invalid_mock.json"),
        ("tests/excel_file_invalid_mock.xlsx","xlsx_file_invalid_mock.xlsx")
    ]) 
    def test_procesar_archivo_no_es_valido(self, archivo, nombre_archivo):
        with open(archivo, "rb") as f:
            procesador = ProcesarArchivoProductos(f, nombre_archivo)
            resultado = procesador.execute()
            assert isinstance(resultado, dict)
            assert "response" in resultado
            assert resultado['response']["msg"] == 'El archivo no contiene las columnas requeridas'
            assert resultado['status_code'] == 400
    
    @pytest.mark.parametrize("archivo,nombre_archivo", [
        ("tests/xml_invalid_mock.xml","xml_invalid_mock.xml")
    ])
    def test_archivo_formato_invalido(self, archivo, nombre_archivo):
        with open(archivo, "rb") as f:
            procesador = ProcesarArchivoProductos(f, nombre_archivo)
            resultado = procesador.execute()
            assert isinstance(resultado, dict)
            assert "response" in resultado
            assert resultado['response']["msg"] == 'Formato de archivo no soportado'
            assert resultado['status_code'] == 400