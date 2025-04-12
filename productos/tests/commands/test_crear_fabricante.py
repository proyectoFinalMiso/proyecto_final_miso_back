import pytest
from faker import Faker

from app import app
from src.commands.crear_fabricante import CrearFabricante
from src.commands.base_command import BaseCommand

class TestCrearFabricante():

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'pais': fake.country()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = CrearFabricante(gen_request[0])
        assert isinstance(route, BaseCommand)

    def test_crear_fabricante(self, gen_request):
        # Test to ensure the route creation works
        with app.test_client() as client:
            response_fabricante = client.post('/crear_fabricante', json=gen_request[0])
            assert response_fabricante.status_code == 201
            assert response_fabricante.json["msg"] == "Fabricante creado con exito"

    def test_crear_fabricante_existe(self, gen_request):
        # Test to ensure the route creation works
        with app.test_client() as client:
            response_fabricante = client.post('/crear_fabricante', json=gen_request[0])
            assert response_fabricante.status_code == 400
            assert response_fabricante.json == {"msg": "Fabricante ya existe"}

    def test_crear_fabricante_campos_requeridos(self, gen_request):
        # Test to ensure the route creation works
        with app.test_client() as client:
            request_body = {
                'nombre': gen_request[0]['nombre']
            }
            response_fabricante = client.post('/crear_fabricante', json=request_body)
            assert response_fabricante.status_code == 400
            assert response_fabricante.json == {"msg": "Campos requeridos no cumplidos"}