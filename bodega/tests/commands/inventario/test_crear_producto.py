import pytest
from faker import Faker
from datetime import datetime

from app import app
from src.commands.inventario.crear_producto import CrearProducto

class TestCrearProducto():
    
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
                'cantidad': fake.pyint(min_value=1, max_value=10),
                'sku': fake.pyint(),
                'volumen': fake.pyfloat(min_value=0.1, max_value=10.0),
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request_producto):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = CrearProducto(gen_request_producto[0])
        assert isinstance(route, CrearProducto)

    def test_crear_producto(self, gen_request_producto, gen_request_bodega):
        with app.test_client() as client:

            response_bodega = client.post('/crear_bodega', json=gen_request_bodega[0])
            nombre_bodega = response_bodega.json['bodega']['nombre']

            request_body = gen_request_producto[0]
            request_body['bodega'] = nombre_bodega

            response_producto = client.post('/stock_crear_producto', json=request_body)
            assert response_producto.status_code == 201
            assert response_producto.json["msg"] == "Producto creado correctamente"

