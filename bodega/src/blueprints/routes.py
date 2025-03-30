from flask import Blueprint, jsonify, request

from src.commands.health_check import HealthCheck
from src.commands.bodega.crear_bodega import CrearBodega
from src.commands.bodega.listar_bodega import ListarBodega
from src.commands.bodega.buscador_bodega import BuscadorBodega
from src.commands.bodega.eliminar_bodega import EliminarBodega

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