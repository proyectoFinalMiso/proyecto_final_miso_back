from flask import Blueprint, jsonify, request
from src.commands.listar_fabricantes import ListarFabricantes
from src.commands.crear_fabricante import CrearFabricante
from src.commands.buscar_fabricante import BuscarFabricante
from src.commands.listar_productos import ListarProductos
from src.commands.crear_producto import CrearProducto
from src.commands.buscar_producto import BuscadorProducto
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

@blueprint.get('/producto/buscar_producto')
def buscar_producto():
    body = request.get_json()
    response = BuscadorProducto(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/fabricante/buscar_fabricante')
def buscar_fabricante():
    body = request.get_json()
    response = BuscarFabricante(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/fabricante/listar_fabricantes')
def listar_fabricantes():
    response = ListarFabricantes().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/producto/listar_productos')
def listar_productos():
    response = ListarProductos().execute()
    return jsonify(response['response']), response['status_code']