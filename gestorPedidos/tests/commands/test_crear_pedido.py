import pytest
from app import app
from faker import Faker
from os import getenv
from random import randint

from src.adapters.adaptador_productos import AdaptadorProductos

class TestCrearPedido():

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

    def test_crear_pedido_exitoso(self, gen_request_producto):
        with app.test_client() as client:
            response = client.post('/pedido/crear', json=gen_request_producto[0])
            assert response.status_code == 201
            assert response.json['msg'] == 'Pedido creado con exito'
    
    def test_crear_pedido_sin_campos_requeridos(self, gen_request_producto):
        with app.test_client() as client:
            pedido_incompleto = gen_request_producto[1]
            del pedido_incompleto['vendedor']
            response = client.post('/pedido/crear', json=pedido_incompleto)
            assert response.status_code == 400
            assert response.json['msg'] == 'Campos requeridos no cumplidos'