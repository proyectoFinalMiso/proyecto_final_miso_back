import pytest
from unittest.mock import patch, MagicMock
from faker import Faker

from src.commands.listar_clientes import ListarClientes

fake = Faker()

class TestListarClientes:
    @pytest.fixture
    def clientes_mock(self):
        return [
            MagicMock(
                id=fake.uuid4(),
                nombre=fake.name(),
                correo=fake.email(),
                vendedorAsociado=fake.uuid4()
            ),
            MagicMock(
                id=fake.uuid4(),
                nombre=fake.name(),
                correo=fake.email(),
                vendedorAsociado=fake.uuid4()
            ),
            MagicMock(
                id=fake.uuid4(),
                nombre=fake.name(),
                correo=fake.email(),
                vendedorAsociado=None
            )
        ]
    
    @patch('src.commands.listar_clientes.Cliente.query')
    def test_execute_success(self, mock_query, clientes_mock):
        # Arrange
        mock_query.all.return_value = clientes_mock
        command = ListarClientes()
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 200
        assert "clientes" in result["response"]
        assert len(result["response"]["clientes"]) == len(clientes_mock)
        
        for i, cliente_data in enumerate(result["response"]["clientes"]):
            assert cliente_data["id"] == clientes_mock[i].id
            assert cliente_data["nombre"] == clientes_mock[i].nombre
            assert cliente_data["correo"] == clientes_mock[i].correo
            assert cliente_data["vendedorAsociado"] == clientes_mock[i].vendedorAsociado
        
        mock_query.all.assert_called_once()
    
    @patch('src.commands.listar_clientes.Cliente.query')
    def test_execute_empty_list(self, mock_query):
        # Arrange
        mock_query.all.return_value = []
        command = ListarClientes()
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 200
        assert "clientes" in result["response"]
        assert len(result["response"]["clientes"]) == 0
        mock_query.all.assert_called_once()
    
    @patch('src.commands.listar_clientes.Cliente.query')
    def test_execute_exception(self, mock_query):
        # Arrange
        mock_query.all.side_effect = Exception("DB Error")
        command = ListarClientes()
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 500
        assert "Error al listar clientes" in result["response"]["msg"] 
