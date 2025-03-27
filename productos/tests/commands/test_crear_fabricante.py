import pytest
import json
from faker import Faker

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