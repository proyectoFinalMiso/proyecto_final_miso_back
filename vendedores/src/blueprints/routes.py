from flask import Blueprint, jsonify, request
from src.commands.health_check import HealthCheck
from src.commands.crear_vendedor import CrearVendedor
from src.commands.obtener_vendedor import ObtenerVendedor

blueprint = Blueprint('productos', __name__)

@blueprint.get('/vendedor/ping')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/vendedor/crear_vendedor')
def crear_vendedor():
    body = request.get_json()
    response = CrearVendedor(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/vendedor/obtener_vendedor')
def obtener_vendedor():
    body = request.get_json()
    response = ObtenerVendedor(body).execute()
    return jsonify(response['response']), response['status_code']