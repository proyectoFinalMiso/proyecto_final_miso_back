from flask import Blueprint, jsonify, request
from src.commands.crear_pedido import CrearPedido
from src.commands.crear_packingList import CrearPackingList
from src.commands.health_check import HealthCheck

blueprint = Blueprint('gestorPedidos', __name__)

@blueprint.get('/health')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/pedido/crear')
def crear_pedido():
    body = request.get_json()
    response = CrearPedido(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/packingList/crear')
def crear_packing_list():
    body = request.get_json()
    response = CrearPackingList(body).execute()
    return jsonify(response['response']), response['status_code']