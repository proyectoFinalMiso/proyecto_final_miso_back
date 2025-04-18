import pytest
import json
from datetime import datetime
from faker import Faker

from app import app
from src.commands.inventario.crear_producto import CrearProducto
from src.commands.inventario.listar_inventario import ListarInventarios
from src.commands.base_command import BaseCommand


class TestListarInventarios():

    @pytest.fixture(scope="module")
    def gen_request_bodega(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                "nombre": fake.name(),
                "direccion": fake.name(),
                "latitude": fake.latitude(),
                "longitude": fake.longitude()
            }
            request_bodies.append(request_body)

        return request_bodies

    @pytest.fixture(scope="module")
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'valorUnitario': fake.pyfloat(),
                'lote': fake.name(),
                'cantidad': fake.pyint(min_value=1, max_value=10),
                'sku': fake.pyint(),
                'volumen': fake.pyfloat(min_value=0.1, max_value=10.0),
            }
            request_bodies.append(request_body)

        return request_bodies

    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = ListarInventarios()
        assert isinstance(route, BaseCommand)

    def test_listar_inventarios(self, gen_request, gen_request_bodega):
        with app.test_client() as client:
            response_bodega = client.post("/crear_bodega", json=gen_request_bodega[0])
            id_bodega = response_bodega.json['bodega']['nombre']

            request_body = gen_request[0]
            request_body['bodega'] = id_bodega

            response_inventario = client.post("/stock_crear_producto", json=request_body)
            assert response_inventario.status_code == 201

            # Luego listamos los inventarios
            response_listar_inventarios = client.get("/stock_listar_inventarios")
            assert response_listar_inventarios.status_code == 200
            assert len(response_listar_inventarios.json) > 0
