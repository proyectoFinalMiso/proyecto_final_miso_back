import pytest
import json
from faker import Faker

from app import app
from src.commands.posicion.buscar_posicion import BuscarPosicion
from src.commands.base_command import BaseCommand


class TestBuscarPosicion():

    @pytest.fixture(scope='module')
    def gen_request_posicion(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'volumen': fake.pyfloat(),
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture(scope='module')
    def gen_request_bodega(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'direccion': fake.name(),
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request_posicion):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = BuscarPosicion({"id_posicion": "1"})
        assert isinstance(route, BaseCommand)

    def test_buscar_posicion(self, gen_request_posicion, gen_request_bodega):
        with app.test_client() as client:

            response_bodega = client.post('/bodega/crear_bodega', json=gen_request_bodega[0])
            id_bodega = response_bodega.json['bodega']['id']

            request_body = gen_request_posicion[0]
            request_body['bodega'] = id_bodega

            response_posicion = client.post('/posicion/crear_posicion', json=request_body)

            id_posicion = response_posicion.json['id']

            response_buscar_posicion = client.get('/posicion/buscar_posicion', json={"id_posicion": id_posicion})
            assert response_buscar_posicion.status_code == 200