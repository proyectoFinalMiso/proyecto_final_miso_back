import pytest
from app import app
from os import getenv

from src.adapters.adaptador_productos import AdaptadorProductos

class TestCrearPackingList():
    def test_conexion_adaptador_productos(self):
        assert getenv("MS_PRODUCTOS_URL")
        adaptador = AdaptadorProductos(getenv("MS_PRODUCTOS_URL"))
        response_servicio = adaptador.comprobar_estado_servicio()
        assert response_servicio
    
    def test_listado_productos(self):
        assert getenv("MS_PRODUCTOS_URL")
        adaptador = AdaptadorProductos(getenv("MS_PRODUCTOS_URL"))
        productos = adaptador.listar_productos()
        assert len(productos) >= 0
        producto_test = productos[15]
        confirmacion_reponse = adaptador.confirmar_producto_existe(producto_test['sku'])
        assert confirmacion_reponse