from app import app
from os import getenv
from random import randint

from src.adapters.adaptador_productos import AdaptadorProductos
from src.models.model import PackingList, db

class TestCrearPackingList():
    def test_conexion_adaptador_productos(self):
        assert getenv("MS_PRODUCTOS_URL")
        adaptador = AdaptadorProductos(getenv("MS_PRODUCTOS_URL"))
        response_servicio = adaptador.comprobar_estado_servicio()
        assert response_servicio
    
    def test_listado_productos(self):
        adaptador = AdaptadorProductos(getenv("MS_PRODUCTOS_URL"))
        productos = adaptador.listar_productos()

        producto_1 = productos[randint(0, len(productos) - 1)]['sku']
        producto_2 = productos[randint(0, len(productos) - 1)]['sku']
        producto_3 = productos[randint(0, len(productos) - 1)]['sku']
        lista_productos = [
            {'sku': producto_1, 'cantidad': 15},
            {'sku': producto_2, 'cantidad': 23},
            {'sku': producto_3, 'cantidad': 4},
        ]

        with app.test_client() as client:
            response = client.post('/packingList/crear', json=lista_productos)
            assert response.status_code == 201
            assert response.json['msg'] == 'Packing list creado con exito'
            
            packing_list_id = response.json['body']['listID']
            valor_factura = response.json['body']['valorFactura']
            valor_calculado = 0
            for producto in lista_productos:
                packing_list = db.session.query(PackingList).filter_by(listID=packing_list_id, producto=producto['sku']).first()
                assert packing_list
                valor_calculado += packing_list.costoTotal
            assert valor_calculado == valor_factura
    
    def test_listado_productos_no_existe(self):
        lista_productos = [
            {'sku': 999999999, 'cantidad': randint(1, 50)},
        ]

        with app.test_client() as client:
            response = client.post('/packingList/crear', json=lista_productos)
            assert response.status_code == 400
            assert response.json['msg'] == 'Hay productos que no existen en el sistema'