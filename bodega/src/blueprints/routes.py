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

blueprint = Blueprint('gestorPedidos', __name__)

@blueprint.get('/bodega/ping')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/bodega/crear_bodega')
def crear_bodega():
    request_body = request.get_json()
    response = CrearBodega(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/bodega/listar_bodegas')
def listar_bodega():
    response = ListarBodega().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/bodega/buscador_bodega')
def buscar_bodega():
    request_body = request.get_json()
    response = BuscadorBodega(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.put('/bodega/eliminar_bodega')
def eliminar_bodega():
    request_body = request.get_json()
    response = EliminarBodega(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/posicion/crear_posicion')
def crear_posicion():
    request_body = request.get_json()
    response = CrearPosicion(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/posicion/listar_posiciones')
def listar_posiciones():
    response = ListarPosicion().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/posicion/buscar_posicion')
def buscar_posicion():
    request_body = request.get_json()
    response = BuscarPosicion(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/inventario/crear_producto')
def crear_producto():
    request_body = request.get_json()
    response = CrearProducto(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/inventario/ingresar_inventario')
def ingresar_inventario():
    request_body = request.get_json()
    response = IngresarInventario(request_body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/inventario/listar_inventarios')
def listar_inventarios():
    response = ListarInventarios().execute()
    return jsonify(response['response']), response['status_code']
