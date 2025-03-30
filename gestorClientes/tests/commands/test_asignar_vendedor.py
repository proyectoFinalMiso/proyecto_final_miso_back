import pytest
from unittest.mock import patch, MagicMock
from faker import Faker

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
    
    @patch('src.commands.asignar_vendedor.Cliente.query')
    def test_execute_cliente_no_encontrado(self, mock_query, cliente_id, vendedor_id):
        # Arrange
        mock_query.filter_by.return_value.first.return_value = None
        command = AsignarVendedor(cliente_id, vendedor_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 404
        assert "Cliente no encontrado" in result["response"]["msg"]
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
    
    @patch('src.commands.asignar_vendedor.Cliente.query')
    def test_execute_success(self, mock_query, cliente_mock, cliente_id, vendedor_id, mock_db_session):
        # Arrange
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
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
        mock_db_session.commit.assert_called_once()
    
    @patch('src.commands.asignar_vendedor.Cliente.query')
    def test_execute_exception(self, mock_query, cliente_mock, cliente_id, vendedor_id, mock_db_session):
        # Arrange
        mock_query.filter_by.return_value.first.return_value = cliente_mock
        mock_db_session.commit.side_effect = Exception("DB Error")
        command = AsignarVendedor(cliente_id, vendedor_id)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 500
        assert "Error al asignar vendedor" in result["response"]["msg"]
        mock_query.filter_by.assert_called_once_with(id=cliente_id)
        mock_db_session.rollback.assert_called_once()
