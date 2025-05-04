import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from datetime import datetime

from src.commands.registrar_visita import RegistrarVisita

fake = Faker()

class TestRegistrarVisita:
    @pytest.fixture
    def cliente_id(self):
        return fake.uuid4()

    @pytest.fixture
    def vendedor_id(self):
        return fake.uuid4()

    @pytest.fixture
    def visita_data(self, vendedor_id):
        return {
            "vendedor_id": str(vendedor_id),
            "fecha": datetime.now().isoformat(),
            "estado": "programada"
        }

    @pytest.fixture
    def mock_db_session(self):
        with patch('src.commands.registrar_visita.db.session') as mock_session:
            yield mock_session

    @pytest.fixture(autouse=True)
    def patch_datetime_and_visita(self):
        # Mock datetime.now() para que siempre sea 2025-04-29
        with patch('src.commands.registrar_visita.datetime') as mock_datetime, \
             patch('src.commands.registrar_visita.Visita') as mock_visita:
            mock_datetime.now.return_value = datetime(2025, 4, 29, 12, 0, 0)
            mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
            # Por defecto, no hay visitas existentes (para no fallar por duplicidad)
            mock_visita.query.filter_by.return_value.first.return_value = None
            yield

    def test_check_campos_requeridos_success(self, cliente_id, visita_data):
        command = RegistrarVisita(cliente_id, visita_data)
        assert command.check_campos_requeridos() is True

    def test_check_campos_requeridos_missing_field(self, cliente_id, visita_data):
        data = visita_data.copy()
        data.pop("estado")
        command = RegistrarVisita(cliente_id, data)
        assert command.check_campos_requeridos() is False

    def test_validate_date_format_valid(self, cliente_id, visita_data):
        command = RegistrarVisita(cliente_id, visita_data)
        date_obj = command.validate_date_format(visita_data["fecha"])
        assert isinstance(date_obj, datetime)

    def test_validate_date_format_invalid(self, cliente_id, visita_data):
        command = RegistrarVisita(cliente_id, visita_data)
        assert command.validate_date_format("not-a-date") is None

    @patch('src.commands.registrar_visita.requests.get')
    @patch('src.commands.registrar_visita.os.getenv')
    def test_verificar_vendedor_existe_true(self, mock_getenv, mock_get, cliente_id, visita_data):
        mock_getenv.return_value = "http://test-url:3001"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        command = RegistrarVisita(cliente_id, visita_data)
        assert command.verificar_vendedor_existe() is True

    @patch('src.commands.registrar_visita.requests.get')
    @patch('src.commands.registrar_visita.os.getenv')
    def test_verificar_vendedor_existe_false(self, mock_getenv, mock_get, cliente_id, visita_data):
        mock_getenv.return_value = "http://test-url:3001"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        command = RegistrarVisita(cliente_id, visita_data)
        assert command.verificar_vendedor_existe() is False

    @patch('src.commands.registrar_visita.requests.get')
    def test_verificar_vendedor_existe_exception(self, mock_get, cliente_id, visita_data):
        mock_get.side_effect = Exception("Connection error")
        command = RegistrarVisita(cliente_id, visita_data)
        assert command.verificar_vendedor_existe() is False

    @patch('src.commands.registrar_visita.RegistrarVisita.verificar_vendedor_existe')
    def test_execute_campos_requeridos_no_cumplidos(self, mock_verificar, cliente_id, visita_data):
        data = {"vendedor_id": visita_data["vendedor_id"]}  # missing fields
        command = RegistrarVisita(cliente_id, data)
        result = command.execute()
        assert result["status_code"] == 400
        assert "requeridos" in result["response"]["msg"]

    @patch('src.commands.registrar_visita.RegistrarVisita.verificar_vendedor_existe')
    def test_execute_fecha_invalida(self, mock_verificar, cliente_id, visita_data):
        data = visita_data.copy()
        data["fecha"] = "invalid-date"
        command = RegistrarVisita(cliente_id, data)
        result = command.execute()
        assert result["status_code"] == 400
        assert "Formato de fecha inválido" in result["response"]["msg"]

    @patch('src.commands.registrar_visita.RegistrarVisita.verificar_vendedor_existe')
    def test_execute_estado_invalido(self, mock_verificar, cliente_id, visita_data):
        data = visita_data.copy()
        data["estado"] = "NO_EXISTE"
        command = RegistrarVisita(cliente_id, data)
        result = command.execute()
        assert result["status_code"] == 400
        assert "Estado de visita inválido" in result["response"]["msg"]

    @patch('src.commands.registrar_visita.RegistrarVisita.verificar_vendedor_existe')
    def test_execute_vendedor_no_encontrado(self, mock_verificar, cliente_id, visita_data):
        mock_verificar.return_value = False
        command = RegistrarVisita(cliente_id, visita_data)
        result = command.execute()
        assert result["status_code"] == 404
        assert "Vendedor no encontrado" in result["response"]["msg"]

    @patch('src.commands.registrar_visita.RegistrarVisita.verificar_vendedor_existe')
    @patch('src.commands.registrar_visita.Cliente.query')
    def test_execute_cliente_no_encontrado(self, mock_query, mock_verificar, cliente_id, visita_data):
        mock_verificar.return_value = True
        mock_query.filter_by.return_value.first.return_value = None
        command = RegistrarVisita(cliente_id, visita_data)
        result = command.execute()
        assert result["status_code"] == 404
        assert "Cliente no encontrado" in result["response"]["msg"]
        mock_query.filter_by.assert_called_once_with(id=cliente_id)

    @patch('src.commands.registrar_visita.RegistrarVisita.verificar_vendedor_existe')
    @patch('src.commands.registrar_visita.Cliente.query')
    @patch('src.commands.registrar_visita.db.session')
    @patch('src.commands.registrar_visita.Visita')
    def test_execute_success(self, mock_visita, mock_db_session, mock_query, mock_verificar, cliente_id, visita_data):
        mock_verificar.return_value = True
        mock_cliente = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_cliente
        mock_visita_instance = MagicMock()
        mock_visita.return_value = mock_visita_instance
        mock_visita.query.filter_by.return_value.first.return_value = None
        mock_visita_instance.id = fake.uuid4()
        mock_visita_instance.cliente_id = cliente_id
        mock_visita_instance.vendedor_id = visita_data["vendedor_id"]
        mock_visita_instance.fecha = datetime.now()
        mock_visita_instance.estado.value = visita_data["estado"]
        mock_visita_instance.estado = MagicMock()
        mock_visita_instance.estado.value = visita_data["estado"]
        command = RegistrarVisita(cliente_id, visita_data)
        result = command.execute()
        assert result["status_code"] == 200
        assert "Visita registrada correctamente" in result["response"]["msg"]
        assert "visita" in result["response"]
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @patch('src.commands.registrar_visita.RegistrarVisita.verificar_vendedor_existe')
    @patch('src.commands.registrar_visita.Cliente.query')
    @patch('src.commands.registrar_visita.db.session')
    @patch('src.commands.registrar_visita.Visita')
    def test_execute_db_exception(self, mock_visita, mock_db_session, mock_query, mock_verificar, cliente_id, visita_data):
        mock_verificar.return_value = True
        mock_cliente = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_cliente
        mock_visita_instance = MagicMock()
        mock_visita.return_value = mock_visita_instance
        mock_visita.query.filter_by.return_value.first.return_value = None
        mock_db_session.commit.side_effect = Exception("DB Error")
        command = RegistrarVisita(cliente_id, visita_data)
        result = command.execute()
        assert result["status_code"] == 500
        assert "Error al registrar visita" in result["response"]["msg"]
        mock_db_session.rollback.assert_called_once()
