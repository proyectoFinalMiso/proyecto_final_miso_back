import pytest
import json
from faker import Faker

from app import app
from src.commands.buscar_producto import BuscarProducto
from src.commands.base_command import BaseCommand

class TestBuscarProducto():

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'sku': fake.uuid4()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture(scope='module')
    def gen_request_fabricante(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'pais': fake.country()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture(scope='module')
    def gen_request_producto(self):
        fake = Faker()
        Faker.seed(0)
        request_bodies = []

        for i in range(10):
            request_body = {
                'id_fabricante': fake.uuid4(),
                'nombre': fake.name(),
                'valorUnitario': fake.pyfloat()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = BuscarProducto(gen_request[0])
        assert isinstance(route, BaseCommand)

    def test_buscar_producto_no_existe(self, gen_request):
        # Test to ensure the route creation works
        with app.test_client() as client:
            buscar_producto_body = gen_request[0]
            buscar_producto_body['sku'] = '1234567890'

            response = client.post('/producto/buscar_sku', json=buscar_producto_body)
            print(response.json)

            assert response.status_code == 404
            assert response.json['msg'] == 'No se ha encontrado el producto solicitado'

    def test_buscar_producto_campos_requeridos(self, gen_request):
        # Test to ensure the route creation works
        with app.test_client() as client:
            buscar_producto_body = {"campo_malo": "1234567890"}

            response = client.post('/producto/buscar_sku', json=buscar_producto_body)
            print(response.json)

            assert response.status_code == 400
            assert response.json == {'msg':'Solo se pueden buscar productos por medio del SKU'}

    # def test_buscar_producto(self, gen_request_fabricante, gen_request_producto):
    #     # Test to ensure the route creation works
    #     with app.test_client() as client:
    #         response_fabricante = client.post('/fabricante/crear_fabricante', json=gen_request_fabricante[0])
    #         assert response_fabricante.status_code == 201

    #         print(response_fabricante.json)

    #         crear_producto_body = gen_request_producto[0]
    #         crear_producto_body['id_fabricante'] = response_fabricante.json['id']

    #         response_crear_producto = client.post('/producto/crear_producto', json=crear_producto_body)
    #         print(response_crear_producto.json)