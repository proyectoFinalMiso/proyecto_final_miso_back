import pytest
import json
from faker import Faker

from app import app
from src.commands.listar_fabricantes import ListarFabricantes
from src.commands.base_command import BaseCommand


class TestListarFabricantes():

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.company(),
                'pais': fake.country()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request):
        route = ListarFabricantes()
        assert isinstance(route, BaseCommand)

    def test_listar_fabricantes(self, gen_request):
        
        with app.test_client() as client:
            for fabricante in gen_request:
                client.post('/fabricante/crear_fabricante', json=fabricante)
            
            response = client.get('/fabricante/listar_fabricantes')        
            assert response.status_code == 200
            assert len(response.json['body']) > 0

    