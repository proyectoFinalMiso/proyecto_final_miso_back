from flask import Blueprint, jsonify, request
from src.commands.buscar_producto import BuscarProducto
from src.commands.crear_fabricante import CrearFabricante
from src.commands.crear_producto import CrearProducto
from src.commands.buscador_producto import BuscadorProducto
from src.commands.health_check import HealthCheck

blueprint = Blueprint('productos', __name__)

@blueprint.get('/producto/ping')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/fabricante/crear_fabricante')
def crear_fabricante():
    body = request.get_json()
    response = CrearFabricante(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/producto/crear_producto')
def crear_producto():
    body = request.get_json()
    response = CrearProducto(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/producto/buscar_sku')
def buscar_producto():
    body = request.get_json()
    print(body)
    response = BuscarProducto(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/producto/buscador_producto')
def buscador_producto():
    body = request.get_json()
    print(body)
    response = BuscadorProducto(body).execute()
    return jsonify(response['response']), response['status_code']

