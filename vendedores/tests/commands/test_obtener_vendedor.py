import pytest
import json
from faker import Faker

from app import app
from src.commands.obtener_vendedor import ObtenerVendedor
from src.commands.crear_vendedor import CrearVendedor
from src.commands.base_command import BaseCommand

class TestObtenerVendedor():

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
        route = ObtenerVendedor(gen_request[0])
        assert isinstance(route, BaseCommand)

    def test_obtener_vendedor(self, gen_request):
        with app.test_client() as client:
            create_user = client.post('/crear_vendedor', json=gen_request[0])
            response = client.get('/obtener_vendedor', json={'email': gen_request[0]['email']})
            assert response.status_code == 200
            assert response.json['email'] == gen_request[0]['email']
            assert response.json['nombre'] == gen_request[0]['nombre']
            
