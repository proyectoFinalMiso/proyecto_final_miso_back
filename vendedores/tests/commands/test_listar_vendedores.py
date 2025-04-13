import pytest
import json
from datetime import datetime
from faker import Faker

from app import app
from src.commands.listar_vendedores import ListarVendedores
from src.commands.crear_vendedor import CrearVendedor
from src.commands.base_command import BaseCommand


class TestListarVendedors():

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            nombre_random = fake.name()
            request_body = {
                'nombre': nombre_random,
                'email': f'{nombre_random.replace(" ", "")}@ccp.com'
            }
            request_bodies.append(request_body)

        return request_bodies

    def test_base_model_inherit(self, gen_request):
        route = ListarVendedores()
        assert isinstance(route, BaseCommand)


    def test_crear_listar(self, gen_request):
        with app.test_client() as client:
            response_crear = client.post('/crear_vendedor', json=gen_request[0])
            
            response_listar = client.get('/listar_vendedores')
            assert response_listar.status_code == 200
