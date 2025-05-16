from unittest.mock import patch, MagicMock
from faker import Faker

from src.commands.listar_visitas import ListarVisitas

fake = Faker()


class TestListarVisitas:
    @patch("src.commands.listar_visitas.Cliente")
    @patch("src.commands.listar_visitas.Visita")
    @patch("src.commands.listar_visitas.db")
    def test_listar_visitas_query(self, mock_db, mock_visita_model, mock_cliente_model):
        mock_visita = MagicMock()
        mock_visita.id = 1
        mock_visita.cliente_id = 10
        mock_visita.vendedor_id = 20
        mock_visita.estado.value = "pendiente"
        mock_visita.fecha.isoformat.return_value = "2024-01-01T00:00:00"

        mock_cliente = MagicMock()
        mock_cliente.id = 99
        mock_cliente.nombre = "Cliente Prueba"

        query_mock = MagicMock()
        mock_db.session.query.return_value = query_mock
        query_mock.join.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.all.return_value = [(mock_visita, mock_cliente)]

        command = ListarVisitas()
        result = command.execute()

        assert result["status_code"] == 200
        visitas = result["response"]["visitas"]
        assert len(visitas) == 1
        assert visitas[0]["id"] == 1
        assert visitas[0]["cliente_id"] == 99
        assert visitas[0]["cliente_nombre"] == "Cliente Prueba"
