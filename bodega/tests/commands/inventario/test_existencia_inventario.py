import pytest
import json
from faker import Faker

from app import app
from src.commands.inventario.existencia_inventario import ExistenciaInventarioTotales
from src.commands.base_command import BaseCommand
from src.models.model import db, Inventario

class TestNecesidadInventario:

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(3):
            request_body = {
                'sku': fake.random_int(min=10001, max=99999),
                'cantidad': fake.random_int(min=1, max=50),
                'fechaActualizacion': fake.date_time_this_year()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = ExistenciaInventarioTotales()
        assert isinstance(route, BaseCommand)

    def test_listar_inventario_vacio(self, gen_request):
        # Test to ensure the response is empty when there are no records in the database
        with app.app_context():

            route = ExistenciaInventarioTotales()
            response = route.execute()

            assert response['response']['msg'] == 'Inventario total ecnontrado.'
            assert response['status_code'] == 200
