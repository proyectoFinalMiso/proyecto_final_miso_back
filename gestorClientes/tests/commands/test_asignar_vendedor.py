import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
import os

from src.commands.asignar_vendedor import AsignarVendedor
from src.models.model import Cliente

fake = Faker()

class TestAsignarVendedor:
    @pytest.fixture
    def cliente_mock(self):
        return MagicMock(
            id=fake.uuid4(),
            nombre=fake.name(),
            correo=fake.email(),
            vendedorAsociado=None
        )
    
    @pytest.fixture
    def vendedor_id(self):
        return fake.uuid4()

    @pytest.fixture
    def cliente_id(self):
        return fake.uuid4()
    
    @pytest.fixture
    def mock_db_session(self):
        with patch('src.commands.asignar_vendedor.db.session') as mock_session:
            yield mock_session
    
    @patch('src.commands.asignar_vendedor.os.getenv')
    @patch('src.commands.asignar_vendedor.requests.get')
    def test_verificar_vendedor_existe_true(self, mock_get, mock_getenv, vendedor_id):
        # Arrange
        mock_getenv.return_value = "http://test-url:3001"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        command = AsignarVendedor(fake.uuid4(), vendedor_id)
        
        # Act
        result = command.verificar_vendedor_existe()
        
        # Assert
        assert result is True
        mock_getenv.assert_called_once_with("MS_VENDEDOR_URL")
        mock_get.assert_called_once_with(f"http://test-url:3001/obtener_vendedor/{vendedor_id}")
    
    @patch('src.commands.asignar_vendedor.os.getenv')
    @patch('src.commands.asignar_vendedor.requests.get')
    def test_verificar_vendedor_existe_false(self, mock_get, mock_getenv, vendedor_id):
        # Arrange
        mock_getenv.return_value = "http://test-url:3001"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        command = AsignarVendedor(fake.uuid4(), vendedor_id)
        
        # Act
        result = command.verificar_vendedor_existe()
        
        # Assert
        assert result is False
        mock_getenv.assert_called_once_with("MS_VENDEDOR_URL")
        mock_get.assert_called_once_with(f"http://test-url:3001/obtener_vendedor/{vendedor_id}")
    
    @patch('src.commands.asignar_vendedor.requests.get')
    def test_verificar_vendedor_existe_exception(self, mock_get, vendedor_id):
        # Arrange
        mock_get.side_effect = Exception("Connection error")
        command = AsignarVendedor(fake.uuid4(), vendedor_id)
        
        # Act
        result = command.verificar_vendedor_existe()
        
        # Assert
        assert result is False
    
    @patch('src.commands.asignar_vendedor.AsignarVendedor.verificar_vendedor_existe')
    @patch('src.commands.asignar_vendedor.Cliente.query')
    def test_execute_vendedor_no_encontrado(self, mock_query, mock_verificar, cliente_id, vendedor_id):
        # Arrange
        mock_verificar.return_value = False
        command = AsignarVendedor(cliente_id, vendedor_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 404
        assert "Vendedor no encontrado" in result["response"]["msg"]
        mock_verificar.assert_called_once()
        mock_query.filter_by.assert_not_called()
    
    @patch('src.commands.asignar_vendedor.AsignarVendedor.verificar_vendedor_existe')
    @patch('src.commands.asignar_vendedor.Cliente.query')
    def test_execute_cliente_no_encontrado(self, mock_query, mock_verificar, cliente_id, vendedor_id):
        # Arrange
        mock_verificar.return_value = True
        mock_query.filter_by.return_value.first.return_value = None
        command = AsignarVendedor(cliente_id, vendedor_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 404
        assert "Cliente no encontrado" in result["response"]["msg"]
        mock_verificar.assert_called_once()
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
    
    @patch('src.commands.asignar_vendedor.AsignarVendedor.verificar_vendedor_existe')
    @patch('src.commands.asignar_vendedor.Cliente.query')
    def test_execute_success(self, mock_query, mock_verificar, cliente_mock, cliente_id, vendedor_id, mock_db_session):
        # Arrange
        mock_verificar.return_value = True
        mock_query.filter_by.return_value.first.return_value = cliente_mock
        command = AsignarVendedor(cliente_id, vendedor_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 200
        assert "Vendedor asignado correctamente" in result["response"]["msg"]
        assert "cliente" in result["response"]
        assert result["response"]["cliente"]["vendedorAsociado"] == vendedor_id
        assert cliente_mock.vendedorAsociado == vendedor_id
        mock_verificar.assert_called_once()
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
        mock_db_session.commit.assert_called_once()
    
    @patch('src.commands.asignar_vendedor.AsignarVendedor.verificar_vendedor_existe')
    @patch('src.commands.asignar_vendedor.Cliente.query')
    def test_execute_exception(self, mock_query, mock_verificar, cliente_mock, cliente_id, vendedor_id, mock_db_session):
        # Arrange
        mock_verificar.return_value = True
        mock_query.filter_by.return_value.first.return_value = cliente_mock
        mock_db_session.commit.side_effect = Exception("DB Error")
        command = AsignarVendedor(cliente_id, vendedor_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 500
        assert "Error al asignar vendedor" in result["response"]["msg"]
        mock_verificar.assert_called_once()
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
        mock_db_session.rollback.assert_called_once()
