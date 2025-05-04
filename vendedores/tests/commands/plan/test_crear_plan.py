import pytest
import json
from faker import Faker
from datetime import datetime

from app import app
from src.commands.plan.crear_plan import CrearPlanVentas
from src.commands.base_command import BaseCommand
from src.models.model import db, PlanVentas, Vendedor

class TestCrearPlanVentas():
    @pytest.fixture(scope='module')
    def gen_request_vendedor(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            fake_name = fake.name()
            request_body = {
                'id': f'{fake.uuid4()}',
                'nombre': fake_name,
                'email': f'{fake_name.replace(" ", "")}@ccp.com',
                'contrasena': fake.password()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture(scope='module')
    def gen_request_plan(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'vendedor_id': f'{fake.uuid4()}',
                'vendedor_nombre': fake.name(),
                'meta_ventas': fake.random_int(min=1000, max=10000),
                'productos_plan': str([
                        f'{fake.name()}', f'{fake.name()}'
                ])
            }
            request_bodies.append(request_body)

        return request_bodies
    
    def test_base_model_inherit(self, gen_request_plan):
        route = CrearPlanVentas(gen_request_plan[0])
        assert isinstance(route, BaseCommand)

    def test_crear_plan(self, gen_request_vendedor, gen_request_plan):
        with app.test_client() as client:
            # Crear un vendedor
            nuevo_vendedor = Vendedor(
                id=gen_request_vendedor[0]['id'],
                nombre=gen_request_vendedor[0]['nombre'],
                email=gen_request_vendedor[0]['email'],
                contrasena=gen_request_vendedor[0]['contrasena']
            )
            db.session.add(nuevo_vendedor)
            db.session.commit()

            # Crear un plan
            request_body = {
                'vendedor_id': gen_request_vendedor[0]['id'],
                'vendedor_nombre': gen_request_vendedor[0]['nombre'],
                'meta_ventas': gen_request_plan[0]['meta_ventas'],
                'productos_plan': gen_request_plan[0]['productos_plan']
            }
            print(request_body)
            response = client.post('/crear_plan_ventas', json=request_body)
            print(response)
            assert response.status_code == 201
            assert response.json['msg'] == "Plan de ventas creado exitosamente"
