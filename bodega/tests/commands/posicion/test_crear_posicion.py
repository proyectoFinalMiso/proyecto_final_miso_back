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
                'nombre_posicion': fake.name(),
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
                'latitude': fake.latitude(),
                'longitude': fake.longitude()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request_posicion):
        # Test to ensure RouteCreation inherits from BaseCommand
        route = CrearPosicion(gen_request_posicion[0])
        assert isinstance(route, BaseCommand)

    def test_crear_posicion(self, gen_request_posicion, gen_request_bodega):
        with app.test_client() as client:

            response_bodega = client.post('/crear_bodega', json=gen_request_bodega[0])
            nombre_bodega = response_bodega.json['bodega']['nombre']

            request_body = gen_request_posicion[0]
            request_body['bodega'] = nombre_bodega

            response_posicion = client.post('/crear_posicion', json=request_body)
            assert response_posicion.status_code == 201
            assert response_posicion.json["msg"] == "Posicion creada correctamente"