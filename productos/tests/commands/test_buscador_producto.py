import pytest
import json
from faker import Faker

from app import app
from src.commands.buscar_producto import BuscadorProducto
from src.commands.base_command import BaseCommand


class TestBuscadorProducto():

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'clave': fake.uuid4()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = BuscadorProducto(gen_request[0])
        assert isinstance(route, BaseCommand)

    def test_buscar_producto_no_existe(self, gen_request):
        # Test to ensure the route creation works
        with app.test_client() as client:
            response = client.get('/producto/buscador_producto', json=gen_request[0])
        
            assert response.status_code == 404
            assert response.json['msg'] == 'No se ha encontrado el producto solicitado'

    def test_buscar_producto_campos_requeridos(self, gen_request):
        # Test to ensure the route creation works
        with app.test_client() as client:
            response = client.get('/producto/buscador_producto', json={"clave_mal":"1234567890"})
        
            assert response.status_code == 400
            assert response.json['msg'] == 'Clave para buscar producto no valida'

    