import pytest
import json
from faker import Faker

from app import app
from src.commands.bodega.crear_bodega import CrearBodega
from src.commands.bodega.eliminar_bodega import EliminarBodega
from src.commands.base_command import BaseCommand

class TestEliminarBodega():

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
        route = EliminarBodega(gen_request[0])
        assert isinstance(route, BaseCommand)

    def test_eliminar_bodega(self, gen_request):
        with app.test_client() as client:
            # Primero, creamos una bodega para eliminarla después
            response_bodega = client.post('/crear_bodega', json=gen_request[0])
            assert response_bodega.status_code == 201

            # Ahora, eliminamos la bodega
            id_bodega = str(response_bodega.json["bodega"]["id"])

            response_bodega = client.put('/eliminar_bodega', json={"id": id_bodega})
            assert response_bodega.status_code == 200