import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from datetime import datetime

from src.commands.listar_visitas import ListarVisitas

fake = Faker()

class TestListarVisitas:
    @pytest.fixture
    def visitas_mock(self):
        return [
            MagicMock(
                id=fake.uuid4(),
                cliente_id=fake.uuid4(),
                vendedor_id=fake.uuid4(),
                estado=MagicMock(value="PROGRAMADA"),
                fecha=datetime.now()
            ),
            MagicMock(
                id=fake.uuid4(),
                cliente_id=fake.uuid4(),
                vendedor_id=fake.uuid4(),
                estado=MagicMock(value="COMPLETADA"),
                fecha=datetime.now()
            )
        ]

    @patch('src.commands.listar_visitas.Visita.query')
    def test_execute_success(self, mock_query, visitas_mock):
        mock_query.filter_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = visitas_mock
        command = ListarVisitas()
        result = command.execute()
        assert result["status_code"] == 200
        assert "visitas" in result["response"]
        assert len(result["response"]["visitas"]) == len(visitas_mock)
        for i, visita_data in enumerate(result["response"]["visitas"]):
            assert visita_data["id"] == visitas_mock[i].id
            assert visita_data["cliente_id"] == visitas_mock[i].cliente_id
            assert visita_data["vendedor_id"] == visitas_mock[i].vendedor_id
            assert visita_data["estado"] == visitas_mock[i].estado.value
            assert visita_data["fecha"] == visitas_mock[i].fecha.isoformat()
        mock_query.all.assert_called_once()

    @patch('src.commands.listar_visitas.Visita.query')
    def test_execute_empty_list(self, mock_query):
        mock_query.filter_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []
        command = ListarVisitas()
        result = command.execute()
        assert result["status_code"] == 200
        assert "No se encontraron visitas" in result["response"]["msg"]
        mock_query.all.assert_called_once()

    @patch('src.commands.listar_visitas.Visita.query')
    def test_execute_exception(self, mock_query):
        mock_query.filter_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.side_effect = Exception("DB Error")
        command = ListarVisitas()
        result = command.execute()
        assert result["status_code"] == 500
        assert "DB Error" in result["response"]["msg"]
