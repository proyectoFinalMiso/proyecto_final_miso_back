from flask import Blueprint, jsonify, request
from src.commands.health_check import HealthCheck
from src.commands.crear_vendedor import CrearVendedor

blueprint = Blueprint('productos', __name__)

@blueprint.get('/ping')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/crear_vendedor')
def crear_vendedor():
    body = request.get_json()
    response = CrearVendedor(body).execute()
    return jsonify(response['response']), response['status_code']