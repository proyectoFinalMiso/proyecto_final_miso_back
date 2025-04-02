import pytest
import json
from faker import Faker

from app import app
from src.commands.listar_productos import ListarProductos
from src.commands.base_command import BaseCommand


class TestListarProductos():

    @pytest.fixture(scope='module')
    def gen_request_fabricante(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.company(),
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
    
    def test_base_model_inherit(self):
        route = ListarProductos()
        assert isinstance(route, BaseCommand)

    def test_listar_productos(self, gen_request_fabricante, gen_request_producto):
        
        with app.test_client() as client:
            client.post('/fabricante/crear_fabricante', json=gen_request_fabricante[0])
            fabricante = client.post('/fabricante/buscar_fabricante', json=gen_request_fabricante[0])
            print(fabricante)
            for producto in gen_request_producto:
                producto['id_fabricante'] = fabricante.json['body']['id']
                client.post('/producto/crear_producto', json=producto)
            
            response = client.get('/producto/listar_productos')        
            assert response.status_code == 200
            assert len(response.json['body']) > 0

    