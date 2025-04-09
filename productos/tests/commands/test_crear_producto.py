import pytest
from faker import Faker

from app import app
from src.commands.crear_producto import CrearProducto
from src.commands.base_command import BaseCommand

class TestCrearProducto():
    
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
                'valorUnitario': fake.pyfloat(),
                'volumen': fake.pyfloat()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    
    def test_base_model_inherit(self, gen_request_producto):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = CrearProducto(gen_request_producto[0])
        assert isinstance(route, BaseCommand)

    def test_crear_producto(self, gen_request_fabricante, gen_request_producto):
        # Test to ensure the route creation works
        with app.test_client() as client:
            response_fabricante = client.post('/crear_fabricante', json=gen_request_fabricante[0])
            assert response_fabricante.status_code == 201

            print(response_fabricante.json)

            crear_producto_body = gen_request_producto[0]
            crear_producto_body['id_fabricante'] = response_fabricante.json['id']

            response = client.post('/crear_producto', json=crear_producto_body)
            print(response.json)
            assert response.status_code == 201
            assert response.json == {"msg": "Producto creado exitosamente"}

    def test_crear_producto_existe(self, gen_request_fabricante, gen_request_producto):
        # Test to ensure the route creation works
        with app.test_client() as client:
            response_fabricante = client.post('/crear_fabricante', json=gen_request_fabricante[1])
            assert response_fabricante.status_code == 201

            print(response_fabricante.json)

            crear_producto_body = gen_request_producto[0]
            crear_producto_body['id_fabricante'] = response_fabricante.json['id']

            client.post('/crear_producto', json=crear_producto_body)

            response_bad = client.post('/crear_producto', json=crear_producto_body)
            print(response_bad.json)
            assert response_bad.status_code == 400
            assert response_bad.json == {"msg": "Producto ya existe"}

    def test_crear_producto_campos_requeridos(self, gen_request_fabricante, gen_request_producto):

        # Test to ensure the route creation works
        with app.test_client() as client:
            response_fabricante = client.post('/crear_fabricante', json=gen_request_fabricante[2])
            assert response_fabricante.status_code == 201

            crear_producto_body = gen_request_producto[0]
            crear_producto_body['id_fabricante'] = response_fabricante.json['id']
            crear_producto_body.pop('nombre')

            response = client.post('/crear_producto', json=crear_producto_body)
            
            assert response.status_code == 400
            assert response.json == {"msg": "Campos requeridos no cumplidos"}