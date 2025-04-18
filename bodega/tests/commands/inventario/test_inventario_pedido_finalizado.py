import pytest
from app import app
from datetime import datetime
from faker import Faker

from src.models.model import Inventario, NecesidadCompras, db

class TestInventarioPedidoFinalizado():
    
    @pytest.fixture(scope='module')
    def gen_request_bodega(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'direccion': fake.name(),
                'latitude': fake.latitude(),
                'longitude': fake.longitude()
            }
            request_bodies.append(request_body)

        return request_bodies
    
    @pytest.fixture(scope='module')
    def gen_request_producto(self):
        fake = Faker()
        request_bodies = []

        for i in range(10):
            request_body = {
                'nombre': fake.name(),
                'valorUnitario': fake.pyfloat(),
                'lote': fake.name(),
                'volumen': fake.pyfloat(min_value=0.1, max_value=0.5),
            }
            request_bodies.append(request_body)

        return request_bodies

    def test_generar_reservas_inventario(self, gen_request_bodega, gen_request_producto):
        producto_1 = gen_request_producto[0]
        producto_1['sku'] = 10007
        producto_1['cantidad'] = 137

        producto_2 = gen_request_producto[1]
        producto_2['sku'] = 10008
        producto_2['cantidad'] = 34

        producto_3 = gen_request_producto[2]
        producto_3['sku'] = 10009
        producto_3['cantidad'] = 25

        productos = [producto_1, producto_2, producto_3]    

        productos_reservar = [
                {"sku": 10007, "cantidad": 100},
                {"sku": 10008, "cantidad": 56},
                {"sku": 10009, "cantidad": 25}
            ]

        with app.test_client() as client:
            response_bodega = client.post('/crear_bodega', json=gen_request_bodega[0])
            nombre_bodega = response_bodega.json['bodega']['nombre']

            for producto in productos:
                request_body = producto
                request_body['bodega'] = nombre_bodega
                response_producto = client.post('/stock_crear_producto', json=request_body)
                assert response_producto.status_code == 201
            
            response_reserva = client.post('/stock_reservar_inventario', json=productos_reservar)
            assert response_reserva.status_code == 201

            producto_1_pre = db.session.query(Inventario).filter_by(sku=10007).first()
            producto_2_pre = db.session.query(Inventario).filter_by(sku=10008).first()
            producto_3_pre = db.session.query(Inventario).filter_by(sku=10009).first()

            producto_1_pre_necesidad = db.session.query(NecesidadCompras).filter_by(sku = 10007).first()
            producto_2_pre_necesidad = db.session.query(NecesidadCompras).filter_by(sku = 10008).first()
            producto_3_pre_necesidad = db.session.query(NecesidadCompras).filter_by(sku = 10009).first()

            assert producto_1_pre.cantidadDisponible == 37
            assert producto_1_pre.cantidadReservada == 100
            assert not producto_1_pre_necesidad

            assert producto_2_pre.cantidadDisponible == 0
            assert producto_2_pre.cantidadReservada == 34
            assert producto_2_pre_necesidad.cantidad == 22
            
            assert producto_3_pre.cantidadDisponible == 0
            assert producto_3_pre.cantidadReservada == 25
            assert not producto_3_pre_necesidad

            response_reserva = client.post('/inventario_pedido_finalizado', json=productos_reservar)
            print(response_reserva.json)
            assert response_reserva.status_code == 201
            assert response_reserva.json['msg'] == 'Se ha actualizado la reserva de productos en el sistema por la finalización de un pedido'

            producto_1_post = db.session.query(Inventario).filter_by(sku=10007).first()
            producto_2_post = db.session.query(Inventario).filter_by(sku=10008).first()
            producto_3_post = db.session.query(Inventario).filter_by(sku=10009).first()

            producto_1_post_necesidad = db.session.query(NecesidadCompras).filter_by(sku=10007).first()
            producto_2_post_necesidad = db.session.query(NecesidadCompras).filter_by(sku=10008).first()
            producto_3_post_necesidad = db.session.query(NecesidadCompras).filter_by(sku=10009).first()

            assert producto_1_post.cantidadDisponible == 37
            assert producto_1_post.cantidadReservada == 0
            assert not producto_1_post_necesidad

            assert producto_2_post.cantidadDisponible == 0
            assert producto_2_post.cantidadReservada == 34
            assert producto_2_post_necesidad.cantidad == 22
            
            assert producto_3_post.cantidadDisponible == 0
            assert producto_3_post.cantidadReservada == 0
            assert not producto_3_post_necesidad
    
    def test_campos_requeridos(self):
        productos_reservar = [
                {"sku": 10007, "cantidad": 100},
                {"sku": 10008, "cantidad": 56},
                {"sku": 10009}
            ]    

        with app.test_client() as client:
            response_reserva = client.post('/inventario_pedido_finalizado', json=productos_reservar)
            assert response_reserva.status_code == 400
            assert response_reserva.json == {"msg": "Campos requeridos no cumplidos"}