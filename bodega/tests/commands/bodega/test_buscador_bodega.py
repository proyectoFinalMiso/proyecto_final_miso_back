import pytest
import json
from faker import Faker

from app import app
from src.commands.bodega.crear_bodega import CrearBodega
from src.commands.bodega.buscador_bodega import BuscadorBodega
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
        route = BuscadorBodega({"clave":gen_request[0]['nombre']})
        assert isinstance(route, BaseCommand)

    def test_listar_bodega(self, gen_request):
        with app.test_client() as client:
            response_bodega = client.post('/crear_bodega', json=gen_request[0])
            assert response_bodega.status_code == 201
            response_listar_bodega = client.get('/buscador_bodega', json={"clave":gen_request[0]['nombre']})
            assert response_listar_bodega.status_code == 200

    def test_listar_bodega_vacia(self, gen_request):
        with app.test_client() as client:
            response_listar_bodega = client.get('/buscador_bodega', json={"clave":"no existe"})
            assert response_listar_bodega.status_code == 404

    def test_listar_bodega_campos_requeridos(self, gen_request):
        with app.test_client() as client:
            response_listar_bodega = client.get('/buscador_bodega', json={})
            assert response_listar_bodega.status_code == 400