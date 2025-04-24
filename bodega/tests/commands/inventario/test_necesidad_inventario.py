import pytest
import json
from faker import Faker

from app import app
from src.commands.inventario.necesidad_inventario import NecesidadInventario
from src.commands.base_command import BaseCommand
from src.models.model import db, NecesidadCompras

class TestNecesidadInventario():

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

    def test_base_model_inherit(self, gen_request):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = NecesidadInventario()
        assert isinstance(route, BaseCommand)

    def test_listar_necesidad_inventario(self, gen_request):
        # Test to ensure the command returns a list of necesidades de inventario
        crear_necesidad = NecesidadCompras(
            sku=gen_request[0]['sku'],
            cantidad=gen_request[0]['cantidad'],
            fechaActualizacion=gen_request[0]['fechaActualizacion']
        )
        db.session.add(crear_necesidad)
        db.session.commit()

        with app.app_context():
            necesidad_inventario = NecesidadInventario()
            response = necesidad_inventario.execute()

            assert response['status_code'] == 200
            assert 'msg' in response['response']
            assert 'body' in response['response']
            assert isinstance(response['response']['body'], list)
            assert len(response['response']['body']) > 0
