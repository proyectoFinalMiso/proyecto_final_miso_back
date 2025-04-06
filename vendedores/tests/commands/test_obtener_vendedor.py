import pytest
import json
from faker import Faker
from uuid import uuid4

from app import app
from src.commands.obtener_vendedor import ObtenerVendedor
from src.commands.crear_vendedor import CrearVendedor
from src.commands.base_command import BaseCommand
from src.models.model import Vendedor

class TestObtenerVendedor():

    @pytest.fixture(scope='module')
    def gen_request(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            nombre_random = fake.name()
            request_body = {
                'nombre': nombre_random,
                'email': f'{nombre_random.replace(" ", "")}@ccp.com'
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture
    def vendedor_id(self):
        return str(uuid4())
    
    def test_base_model_inherit(self, vendedor_id):
        route = ObtenerVendedor(vendedor_id)
        assert isinstance(route, BaseCommand)

    def test_verificar_vendedor_existe_false(self, vendedor_id):
        command = ObtenerVendedor(vendedor_id)
        result = command.verificar_vendedor_existe()
        assert result is False
    
    @pytest.mark.parametrize("id_existe", [True, False])
    def test_execute(self, id_existe, vendedor_id, monkeypatch):
        # Arrange
        command = ObtenerVendedor(vendedor_id)
        
        if id_existe:
            vendedor_mock = type('', (), {})()
            vendedor_mock.id = vendedor_id
            vendedor_mock.nombre = "Test Name"
            vendedor_mock.email = "test@ccp.com"
            monkeypatch.setattr(command, 'verificar_vendedor_existe', lambda: vendedor_mock)
            
            # Act
            result = command.execute()
            
            # Assert
            assert result["status_code"] == 200
            assert result["response"]["id"] == vendedor_id
            assert result["response"]["nombre"] == "Test Name"
            assert result["response"]["email"] == "test@ccp.com"
        else:
            monkeypatch.setattr(command, 'verificar_vendedor_existe', lambda: False)
            
            # Act
            result = command.execute()
            
            # Assert
            assert result["status_code"] == 404
            assert "Vendedor no existe" in result["response"]["msg"]

    def test_integration_obtener_vendedor(self, gen_request):
        with app.test_client() as client:
            # Crear un vendedor primero
            response_create = client.post('/crear_vendedor', json=gen_request[1])
            create_data = json.loads(response_create.data)
            assert "msg" in create_data
            assert response_create.status_code == 201
            
            # Obtener el ID del vendedor desde la base de datos
            vendedor = Vendedor.query.filter_by(email=gen_request[1]['email']).first()
            assert vendedor is not None
            
            # Obtener el vendedor creado usando su ID
            response_get = client.get(f'/obtener_vendedor/{vendedor.id}')
            
            # Assert
            assert response_get.status_code == 200
            data = json.loads(response_get.data)
            assert data["id"] == vendedor.id
            assert data["nombre"] == gen_request[1]["nombre"]
            assert data["email"] == gen_request[1]["email"]
            
