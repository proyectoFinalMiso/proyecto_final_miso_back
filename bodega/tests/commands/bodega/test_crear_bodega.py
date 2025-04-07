import pytest
import json
from faker import Faker

from app import app
from src.commands.bodega.crear_bodega import CrearBodega
from src.commands.base_command import BaseCommand

class TestCrearBodega():

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
        route = CrearBodega(gen_request[0])
        assert isinstance(route, BaseCommand)

    def test_crear_bodega_campos_requeridos(self, gen_request):
        with app.test_client() as client:
            request_body = {
                'nombre': gen_request[0]['nombre']
            }
            response_bodega = client.post('/crear_bodega', json=request_body)
            assert response_bodega.status_code == 400
            assert response_bodega.json == {"msg": "Campos requeridos no cumplidos"}
    
    def test_crear_bodega(self, gen_request):
        with app.test_client() as client:
            response_bodega = client.post('/crear_bodega', json=gen_request[0])
            assert response_bodega.status_code == 201
            # assert response_bodega.json["msg"] == "Bodega creada con exito"