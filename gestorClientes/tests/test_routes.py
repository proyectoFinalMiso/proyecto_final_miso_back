import pytest
import json
from unittest.mock import patch, MagicMock
from faker import Faker

fake = Faker()

class TestRoutes:
    @pytest.fixture
    def cliente_data(self):
        return {
            "nombre": fake.name(),
            "correo": fake.email()
        }
    
    @pytest.fixture
    def cliente_mock(self):
        return {
            "id": fake.uuid4(),
            "nombre": fake.name(),
            "correo": fake.email(),
            "vendedorAsociado": fake.uuid4()
        }
    
    def test_health_check(self, client):
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert "message" in data
        assert data["message"] == "pong"
    
    @patch('src.commands.crear_cliente.CrearCliente.execute')
    def test_crear_cliente(self, mock_execute, cliente_data, client):
        cliente_id = fake.uuid4()
        mock_execute.return_value = {
            "response": {
                "msg": "Cliente creado con éxito",
                "id": cliente_id
            },
            "status_code": 201
        }
        
        response = client.post('/crear', 
                              json=cliente_data, 
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data.decode('utf-8'))
        assert "msg" in data
        assert data["msg"] == "Cliente creado con éxito"
        assert "id" in data
        assert data["id"] == cliente_id
        mock_execute.assert_called_once()
    
    @patch('src.commands.consultar_cliente.ConsultarCliente.execute')
    def test_consultar_cliente(self, mock_execute, cliente_mock, client):
        cliente_id = cliente_mock["id"]
        mock_execute.return_value = {
            "response": {
                "cliente": cliente_mock
            },
            "status_code": 200
        }
        
        response = client.get(f'/{cliente_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert "cliente" in data
        assert data["cliente"] == cliente_mock
        mock_execute.assert_called_once()
    
    @patch('src.commands.listar_clientes.ListarClientes.execute')
    def test_listar_clientes(self, mock_execute, cliente_mock, client):
        clientes = [cliente_mock, {
            "id": fake.uuid4(),
            "nombre": fake.name(),
            "correo": fake.email(),
            "vendedorAsociado": None
        }]
        
        mock_execute.return_value = {
            "response": {
                "clientes": clientes
            },
            "status_code": 200
        }
        
        response = client.get('/clientes')
        
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert "clientes" in data
        assert data["clientes"] == clientes
        assert len(data["clientes"]) == 2
        mock_execute.assert_called_once()
    
    @patch('src.commands.asignar_vendedor.AsignarVendedor.execute')
    def test_asignar_vendedor(self, mock_execute, cliente_mock, client):
        cliente_id = cliente_mock["id"]
        vendedor_id = fake.uuid4()
        
        cliente_mock["vendedorAsociado"] = vendedor_id
        
        mock_execute.return_value = {
            "response": {
                "msg": "Vendedor asignado correctamente",
                "cliente": cliente_mock
            },
            "status_code": 200
        }
        
        response = client.post(f'/{cliente_id}/asignar_vendedor/{vendedor_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert "msg" in data
        assert data["msg"] == "Vendedor asignado correctamente"
        assert "cliente" in data
        assert data["cliente"] == cliente_mock
        assert data["cliente"]["vendedorAsociado"] == vendedor_id
        mock_execute.assert_called_once()

    @patch('src.commands.generate_upload_url.GenerateUploadUrl.execute')
    def test_generate_upload_url(self, mock_execute, client):
        request_data = {
            "filename": "video.mp4",
            "contentType": "video/mp4",
            "clientId": "client123"
        }
        signed_url = "https://fake-signed-url.com/upload"
        gcs_path = "gs://fake-bucket/video.mp4"
        
        mock_execute.return_value = {
            "response": {
                "signedUrl": signed_url,
                "gcsPath": gcs_path
            },
            "status_code": 200
        }
        
        response = client.post('/generate_upload_url', 
                              json=request_data, 
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert "signedUrl" in data
        assert data["signedUrl"] == signed_url
        assert "gcsPath" in data
        assert data["gcsPath"] == gcs_path
        mock_execute.assert_called_once_with()

    @patch('src.commands.notify_upload_complete.NotifyUploadComplete.execute')
    def test_notify_upload_complete(self, mock_execute, client):
        request_data = {
            "blobPath": "gs://fake-bucket/video.mp4",
            "clientId": "client123",
            "vendedorId": "vendedor456"
        }
        message_id = "pubsub-message-id-123"
        
        mock_execute.return_value = {
            "response": {
                "message": "Upload notification sent successfully.",
                "messageId": message_id
            },
            "status_code": 200
        }
        
        response = client.post('/notify_upload_complete', 
                              json=request_data, 
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert "message" in data
        assert data["message"] == "Upload notification sent successfully."
        assert "messageId" in data
        assert data["messageId"] == message_id
        mock_execute.assert_called_once_with()
