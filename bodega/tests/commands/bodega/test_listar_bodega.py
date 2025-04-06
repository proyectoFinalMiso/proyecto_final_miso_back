import pytest
import json
from faker import Faker

from app import app
from src.commands.bodega.crear_bodega import CrearBodega
from src.commands.bodega.listar_bodega import ListarBodega
from src.commands.base_command import BaseCommand

class TestListarBodega():
        
    @pytest.fixture(scope='module')
    def gen_request(self):
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
    
    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = ListarBodega()
        assert isinstance(route, BaseCommand)

    def test_listar_bodega(self, gen_request):
        with app.test_client() as client:
            # Primero creamos una bodega para luego listar
            response_bodega = client.post('/crear_bodega', json=gen_request[0])
            assert response_bodega.status_code == 201
            # Luego listamos las bodegas
            response_listar_bodega = client.get('/listar_bodegas')
            assert response_listar_bodega.status_code == 200
            assert len(response_listar_bodega.json) > 0