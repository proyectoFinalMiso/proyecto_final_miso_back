from flask import Blueprint, jsonify, request

from src.commands.health_check import HealthCheck
from src.commands.bodega.crear_bodega import CrearBodega
from src.commands.bodega.listar_bodega import ListarBodega
from src.commands.bodega.buscador_bodega import BuscadorBodega
from src.commands.bodega.eliminar_bodega import EliminarBodega
from src.commands.posicion.crear_posicion import CrearPosicion
from src.commands.posicion.listar_posiciones import ListarPosicion
from src.commands.posicion.buscar_posicion import BuscarPosicion
from src.commands.inventario.crear_producto import CrearProducto
from src.commands.inventario.ingresar_inventario import IngresarInventario
from src.commands.inventario.listar_inventario import ListarInventarios
from src.commands.inventario.reservar_inventario import ReservarInventario

blueprint = Blueprint('gestorPedidos', __name__)

@blueprint.get('/ping')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/crear_bodega')
def crear_bodega():
    request_body = request.get_json()
    response = CrearBodega(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/listar_bodegas')
def listar_bodega():
    response = ListarBodega().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/buscador_bodega')
def buscar_bodega():
    request_body = request.get_json()
    response = BuscadorBodega(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.put('/eliminar_bodega')
def eliminar_bodega():
    request_body = request.get_json()
    response = EliminarBodega(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/crear_posicion')
def crear_posicion():
    request_body = request.get_json()
    response = CrearPosicion(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/listar_posiciones')
def listar_posiciones():
    response = ListarPosicion().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/buscar_posicion')
def buscar_posicion():
    request_body = request.get_json()
    response = BuscarPosicion(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/stock_crear_producto')
def crear_producto():
    request_body = request.get_json()
    response = CrearProducto(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/stock_ingresar_inventario')
def ingresar_inventario():
    request_body = request.get_json()
    response = IngresarInventario(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/stock_listar_inventarios')
def listar_inventarios():
    response = ListarInventarios().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/stock_reservar_inventario')
def reservar_inventario():
    request_body = request.get_json()
    response = ReservarInventario(request_body).execute()
    return jsonify(response['response']), response['status_code']