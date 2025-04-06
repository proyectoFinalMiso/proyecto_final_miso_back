import pytest
import json
from faker import Faker
from datetime import datetime

from app import app
from src.commands.inventario.crear_producto import CrearProducto

class TestCrearProducto():

    @pytest.fixture(scope='module')
    def gen_request_posicion(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'volumen': fake.pyfloat(),
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture(scope='module')
    def gen_request_bodega(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'direccion': fake.name(),
                'latitude': fake.latitude(),
                'longitude': fake.longitude()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture(scope='module')
    def gen_request_producto(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'valorUnitario': fake.pyfloat(),
                'lote': fake.name(),
                'cantidad': fake.pyint(),
                'fechaIgreso': datetime.now(),
                'sku': fake.pyint(),
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request_producto):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = CrearProducto(gen_request_producto[0])
        assert isinstance(route, CrearProducto)

    def test_crear_producto(self, gen_request_producto, gen_request_bodega, gen_request_posicion):
        with app.test_client() as client:

            response_bodega = client.post('/crear_bodega', json=gen_request_bodega[0])
            id_bodega = response_bodega.json['bodega']['id']

            request_nody_crear_posicion = gen_request_posicion[0]
            request_nody_crear_posicion['bodega'] = id_bodega

            response_posicion = client.post('/crear_posicion', json=request_nody_crear_posicion)
            id_posicion = response_posicion.json["id"]

            request_body = gen_request_producto[0]
            request_body['bodega'] = id_bodega
            request_body['posicion'] = id_posicion

            response_producto = client.post('/stock_crear_producto', json=request_body)
            assert response_producto.status_code == 201
            assert response_producto.json["msg"] == "Producto creado correctamente"

