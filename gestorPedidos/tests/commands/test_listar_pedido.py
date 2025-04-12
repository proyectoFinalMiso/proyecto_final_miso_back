from app import app

class TestListarPedido():

    def test_listar_pedidos(self):
        with app.test_client() as client:
            response = client.get('/pedidos')
            assert response.status_code == 200
            assert len(response.json['pedidos']) > 0