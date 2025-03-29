import pytest
from unittest.mock import patch, MagicMock
from faker import Faker

from src.commands.consultar_cliente import ConsultarCliente
from src.models.model import Cliente

fake = Faker()

class TestConsultarCliente:
    @pytest.fixture
    def cliente_mock(self):
        return MagicMock(
            id=fake.uuid4(),
            nombre=fake.name(),
            correo=fake.email(),
            vendedorAsociado=fake.uuid4()
        )
    
    def test_check_campos_requeridos_success(self):
        # Arrange
        cliente_id = fake.uuid4()
        command = ConsultarCliente(cliente_id)
        
        # Act
        result = command.check_campos_requeridos()
        
        # Assert
        assert result is True
    
    def test_check_campos_requeridos_failure(self):
        # Arrange
        command = ConsultarCliente(None)
        
        # Act
        result = command.check_campos_requeridos()
        
        # Assert
        assert result is False
    
    def test_execute_sin_id_cliente(self):
        # Arrange
        command = ConsultarCliente(None)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 400
        assert "El ID del cliente es requerido" in result["response"]["msg"]
    
    @patch('src.commands.consultar_cliente.Cliente.query')
    def test_execute_cliente_no_encontrado(self, mock_query):
        # Arrange
        mock_query.filter_by.return_value.first.return_value = None
        cliente_id = fake.uuid4()
        command = ConsultarCliente(cliente_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 404
        assert "Cliente no encontrado" in result["response"]["msg"]
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
    
    @patch('src.commands.consultar_cliente.Cliente.query')
    def test_execute_success(self, mock_query, cliente_mock):
        # Arrange
        mock_query.filter_by.return_value.first.return_value = cliente_mock
        cliente_id = cliente_mock.id
        command = ConsultarCliente(cliente_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 200
        assert "cliente" in result["response"]
        assert result["response"]["cliente"]["id"] == cliente_mock.id
        assert result["response"]["cliente"]["nombre"] == cliente_mock.nombre
        assert result["response"]["cliente"]["correo"] == cliente_mock.correo
        assert result["response"]["cliente"]["vendedorAsociado"] == cliente_mock.vendedorAsociado
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
    
    @patch('src.commands.consultar_cliente.Cliente.query')
    def test_execute_exception(self, mock_query):
        # Arrange
        mock_query.filter_by.side_effect = Exception("DB Error")
        cliente_id = fake.uuid4()
        command = ConsultarCliente(cliente_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 500
        assert "Error al consultar cliente" in result["response"]["msg"] 
