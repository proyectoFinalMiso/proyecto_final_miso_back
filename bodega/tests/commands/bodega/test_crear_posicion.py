import pytest
import json
from faker import Faker

from app import app
from src.commands.posicion.crear_posicion import CrearPosicion
from src.commands.base_command import BaseCommand

class TestCrearPosicion():

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
        route = CrearPosicion(gen_request_posicion[0])
        assert isinstance(route, BaseCommand)

    def test_crear_posicion(self, gen_request_posicion, gen_request_bodega):
        with app.test_client() as client:

            response_bodega = client.post('/bodega/crear_bodega', json=gen_request_bodega[0])
            id_bodega = response_bodega.json['bodega']['id']

            request_body = gen_request_posicion[0]
            request_body['bodega'] = id_bodega

            response_posicion = client.post('/posicion/crear_posicion', json=request_body)
            assert response_posicion.status_code == 201
            assert response_posicion.json["msg"] == "Posicion creada correctamente"