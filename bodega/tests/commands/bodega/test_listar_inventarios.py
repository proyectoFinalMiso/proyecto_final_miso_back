import pytest
import json
from datetime import datetime
from faker import Faker

from app import app
from src.commands.inventario.ingresar_inventario import IngresarInventario
from src.commands.inventario.listar_inventario import ListarInventarios
from src.commands.base_command import BaseCommand


class TestListarInventarios():

    @pytest.fixture(scope="module")
    def gen_request_posicion(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                "volumen": fake.pyfloat(),
            }
            request_bodies.append(request_body)

        return request_bodies

    @pytest.fixture(scope="module")
    def gen_request_bodega(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                "nombre": fake.name(),
                "direccion": fake.name(),
            }
            request_bodies.append(request_body)

        return request_bodies

    @pytest.fixture(scope="module")
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                "nombre": fake.name(),
                "bodega": fake.uuid4(),
                "posicion": fake.uuid4(),
                "valorUnitario": fake.pyfloat(),
                "lote": fake.name(),
                "cantidad": fake.pyint(),
                "fechaIgreso": datetime.now(),
                "sku": fake.pyint(),
            }
            request_bodies.append(request_body)

        return request_bodies

    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = ListarInventarios()
        assert isinstance(route, BaseCommand)

    def test_listar_inventarios(self, gen_request, gen_request_bodega, gen_request_posicion):
        with app.test_client() as client:
            response_bodega = client.post("/bodega/crear_bodega", json=gen_request_bodega[0])
            id_bodega = response_bodega.json['bodega']['id']

            request_body_crear_posicion = gen_request_posicion[0]   
            request_body_crear_posicion['bodega'] = id_bodega

            response_posicion = client.post("/posicion/crear_posicion", json=request_body_crear_posicion)
            print(response_posicion.json)
            id_posicion = response_posicion.json["id"]

            request_body = gen_request[0]
            request_body['bodega'] = id_bodega
            request_body['posicion'] = id_posicion

            response_inventario = client.post("/inventario/crear_producto", json=request_body)
            assert response_inventario.status_code == 201

            # Luego listamos los inventarios
            response_listar_inventarios = client.get("/inventario/listar_inventarios")
            assert response_listar_inventarios.status_code == 200
            assert len(response_listar_inventarios.json) > 0
