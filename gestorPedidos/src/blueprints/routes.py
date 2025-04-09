from flask import Blueprint, jsonify, request
from src.commands.crear_packingList import CrearPackingList
from src.commands.crear_pedido import CrearPedido
from src.commands.crear_ruta_de_entrega import CrearRutaDeEntrega
from src.commands.health_check import HealthCheck
from src.commands.listar_pedidos import ListarPedidos

blueprint = Blueprint('gestorPedidos', __name__)


@blueprint.get('/health')
def health_check():
    return HealthCheck().execute()


@blueprint.post('/pedido/crear')
def crear_pedido():
    body = request.get_json()
    response = CrearPedido(body).execute()
    return jsonify(response['response']), response['status_code']


@blueprint.post('/pedido/ruta_de_entrega')
def crear_ruta_de_entrega():
    body = request.get_json()
    response = CrearRutaDeEntrega(
        body).execute()
    return jsonify(response['response']), response['status_code']


@blueprint.post('/packingList/crear')
def crear_packing_list():
    body = request.get_json()
    response = CrearPackingList(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/pedidos')
def listar_pedidos():
    cliente_id = request.args.get('cliente_id')
    response = ListarPedidos(cliente_id).execute()
    return jsonify(response['response']), response['status_code']
