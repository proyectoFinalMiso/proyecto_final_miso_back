import pytest
from app import app
from faker import Faker
from os import getenv
from random import randint

from src.adapters.adaptador_productos import AdaptadorProductos
from src.models.model import Pedido, db
from src.models.model import EstadoPedido

class TestActualizarEstadoPedido():

    @pytest.fixture(scope='module')
    def gen_request_producto(self):
        fake = Faker()
        request_bodies = []
        adaptador = AdaptadorProductos(getenv("MS_PRODUCTOS_URL"))
        productos = adaptador.listar_productos()

        for i in range(10):

            producto_1 = productos[randint(0, len(productos) - 1)]['sku']
            producto_2 = productos[randint(0, len(productos) - 1)]['sku']
            producto_3 = productos[randint(0, len(productos) - 1)]['sku']
            lista_productos = [
            {'sku': producto_1, 'cantidad': fake.random_number(digits=2, fix_len=False)},
            {'sku': producto_2, 'cantidad': fake.random_number(digits=2, fix_len=False)},
            {'sku': producto_3, 'cantidad': fake.random_number(digits=2, fix_len=False)},
        ]
            request_body = {
                'cliente': '8a0a5ad9-c36c-4d1c-99ce-9a3ea679b23d',
                'vendedor': fake.email(domain='ccp.com'),
                'direccion': fake.address(),
                'latitud': fake.latitude(),
                'longitud': fake.longitude(),
                'productos': lista_productos
            }
            request_bodies.append(request_body)

        return request_bodies

    def test_cambiar_estado_pedido(self, gen_request_producto):
        db.session.query(Pedido).delete()
        with app.test_client() as client:
            response = client.post('/pedido/crear', json=gen_request_producto[0])
            assert response.status_code == 201
            pedido_creado = db.session.query(Pedido).filter(
                Pedido.vendedor == gen_request_producto[0]['vendedor'], 
                Pedido.cliente == gen_request_producto[0]['cliente']).first()
            assert pedido_creado

            cambio_body = {
                'id': pedido_creado.id,
                'estado': 'FINALIZADO'
            }
            response = client.patch('/pedido/actualizar_estado', json=cambio_body)
            assert response.status_code == 200
            assert response.json['msg'] == 'El estado del pedido se actualizó correctamente'
            producto_cambio = response.json['body']

            pedido_cambiado = db.session.query(Pedido).filter(Pedido.id == producto_cambio['id']).first()
            assert pedido_cambiado
            assert pedido_cambiado.estado == EstadoPedido.FINALIZADO
    
    def test_cambiar_estado_pedido_equivocado(self, gen_request_producto):
        db.session.query(Pedido).delete()
        with app.test_client() as client:
            response = client.post('/pedido/crear', json=gen_request_producto[0])
            assert response.status_code == 201
            pedido_creado = db.session.query(Pedido).filter(
                Pedido.vendedor == gen_request_producto[0]['vendedor'], 
                Pedido.cliente == gen_request_producto[0]['cliente']).first()
            assert pedido_creado

            cambio_body = {
                'id': pedido_creado.id,
                'estado': 'REMISIONADO'
            }
            response = client.patch('/pedido/actualizar_estado', json=cambio_body)
            assert response.status_code == 400
            assert response.json['msg'] == 'El estado del pedido debe ser FINALIZADO o CANCELADO'

    def test_cambiar_estado_pedido_campos_incompletos(self, gen_request_producto):
        db.session.query(Pedido).delete()
        with app.test_client() as client:
            response = client.post('/pedido/crear', json=gen_request_producto[0])
            assert response.status_code == 201
            pedido_creado = db.session.query(Pedido).filter(
                Pedido.vendedor == gen_request_producto[0]['vendedor'], 
                Pedido.cliente == gen_request_producto[0]['cliente']).first()
            assert pedido_creado

            cambio_body = {
                'id': pedido_creado.id,
            }
            response = client.patch('/pedido/actualizar_estado', json=cambio_body)
            assert response.status_code == 400
            assert response.json['msg'] == 'La petición no cuenta con todos los campos requeridos'