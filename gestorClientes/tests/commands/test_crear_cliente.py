import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from uuid import UUID

from src.commands.crear_cliente import CrearCliente
from src.models.model import Cliente

fake = Faker()

class TestCrearCliente:
    @pytest.fixture
    def cliente_data(self):
        return {
            "nombre": fake.name(),
            "correo": fake.email(),
            "contrasena": fake.password()
        }

    @pytest.fixture
    def mock_db_session(self):
        with patch('src.commands.crear_cliente.db.session') as mock_session:
            yield mock_session
    
    def test_crear_uuid_returns_valid_uuid(self):
        # Arrange
        command = CrearCliente({})
        
        # Act
        result = command.crear_uuid()
        
        # Assert
        assert isinstance(UUID(result), UUID)
    
    def test_check_campos_requeridos_success(self, cliente_data):
        # Arrange
        command = CrearCliente(cliente_data)
        
        # Act
        result = command.check_campos_requeridos()
        
        # Assert
        assert result is True
    
    def test_check_campos_requeridos_missing_field(self):
        # Arrange
        incomplete_data = {
            "nombre": fake.name(),
            "correo": fake.email()
            # missing contrasena
        }
        command = CrearCliente(incomplete_data)
        
        # Act
        result = command.check_campos_requeridos()
        
        # Assert
        assert result is False
    
    def test_check_campos_requeridos_empty_value(self):
        # Arrange
        invalid_data = {
            "nombre": "",
            "correo": fake.email(),
            "contrasena": fake.password()
        }
        command = CrearCliente(invalid_data)
        
        # Act
        result = command.check_campos_requeridos()
        
        # Assert
        assert result is False
    
    @patch('src.commands.crear_cliente.Cliente.query')
    def test_verificar_cliente_existe_true(self, mock_query, cliente_data):
        # Arrange
        mock_query.filter.return_value.first.return_value = MagicMock()
        command = CrearCliente(cliente_data)
        
        # Act
        result = command.verificar_cliente_existe()
        
        # Assert
        assert result is True
        mock_query.filter.assert_called_once()
    
    @patch('src.commands.crear_cliente.Cliente.query')
    def test_verificar_cliente_existe_false(self, mock_query, cliente_data):
        # Arrange
        mock_query.filter.return_value.first.return_value = None
        command = CrearCliente(cliente_data)
        
        # Act
        result = command.verificar_cliente_existe()
        
        # Assert
        assert result is False
        mock_query.filter.assert_called_once()
    
    @patch('src.commands.crear_cliente.Cliente.query')
    def test_verificar_id_existe_true(self, mock_query):
        # Arrange
        mock_query.filter.return_value.first.return_value = MagicMock()
        command = CrearCliente({})
        test_id = fake.uuid4()
        
        # Act
        result = command.verificar_id_existe(test_id)
        
        # Assert
        assert result is True
        mock_query.filter.assert_called_once()
    
    @patch('src.commands.crear_cliente.Cliente.query')
    def test_verificar_id_existe_false(self, mock_query):
        # Arrange
        mock_query.filter.return_value.first.return_value = None
        command = CrearCliente({})
        test_id = fake.uuid4()
        
        # Act
        result = command.verificar_id_existe(test_id)
        
        # Assert
        assert result is False
        mock_query.filter.assert_called_once()
    
    def test_execute_campos_requeridos_no_cumplidos(self, cliente_data):
        # Arrange
        incomplete_data = {"nombre": cliente_data["nombre"]} # Missing correo
        command = CrearCliente(incomplete_data)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 400
        assert "Campos requeridos no cumplidos" in result["response"]["msg"]
    
    @patch('src.commands.crear_cliente.CrearCliente.check_campos_requeridos')
    @patch('src.commands.crear_cliente.CrearCliente.verificar_cliente_existe')
    def test_execute_cliente_ya_existe(self, mock_verificar_cliente_existe, mock_check_campos_requeridos, cliente_data):
        # Arrange
        mock_check_campos_requeridos.return_value = True
        mock_verificar_cliente_existe.return_value = True
        command = CrearCliente(cliente_data)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 400
        assert "Cliente ya existe" in result["response"]["msg"]
    
    @patch('src.commands.crear_cliente.CrearCliente.check_campos_requeridos')
    @patch('src.commands.crear_cliente.CrearCliente.verificar_cliente_existe')
    @patch('src.commands.crear_cliente.CrearCliente.verificar_id_existe')
    @patch('src.commands.crear_cliente.CrearCliente.crear_uuid')
    @patch('src.commands.crear_cliente.generate_password_hash')
    def test_execute_success(self, mock_hash, mock_crear_uuid, mock_verificar_id_existe, 
                             mock_verificar_cliente_existe, mock_check_campos_requeridos, cliente_data, mock_db_session):
        # Arrange
        mock_check_campos_requeridos.return_value = True
        mock_verificar_cliente_existe.return_value = False
        mock_verificar_id_existe.return_value = False
        mock_uuid = fake.uuid4()
        mock_crear_uuid.return_value = mock_uuid
        mock_hash.return_value = "hashed_password"
        command = CrearCliente(cliente_data)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 201
        assert "Cliente creado con éxito" in result["response"]["msg"]
        assert result["response"]["id"] == mock_uuid
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    @patch('src.commands.crear_cliente.CrearCliente.check_campos_requeridos')
    @patch('src.commands.crear_cliente.CrearCliente.verificar_cliente_existe')
    @patch('src.commands.crear_cliente.CrearCliente.verificar_id_existe')
    @patch('src.commands.crear_cliente.CrearCliente.crear_uuid')
    @patch('src.commands.crear_cliente.generate_password_hash')
    def test_execute_db_exception(self, mock_hash, mock_crear_uuid, mock_verificar_id_existe, 
                                  mock_verificar_cliente_existe, mock_check_campos_requeridos, cliente_data, mock_db_session):
        # Arrange
        mock_check_campos_requeridos.return_value = True
        mock_verificar_cliente_existe.return_value = False
        mock_verificar_id_existe.return_value = False
        mock_uuid = fake.uuid4()
        mock_crear_uuid.return_value = mock_uuid
        mock_hash.return_value = "hashed_password"
        mock_db_session.commit.side_effect = Exception("DB Error")
        command = CrearCliente(cliente_data)
        
        # Act
        result = command.execute()
        
        # Assert
        assert result["status_code"] == 500
        assert "Error al crear cliente" in result["response"]["msg"]
        mock_db_session.rollback.assert_called_once() 
