from flask import Blueprint, jsonify, request
from src.commands.crear_cliente import CrearCliente
from src.commands.consultar_cliente import ConsultarCliente
from src.commands.listar_clientes import ListarClientes
from src.commands.asignar_vendedor import AsignarVendedor
from src.commands.login_cliente import LoginCliente
from src.commands.health_check import HealthCheck

blueprint = Blueprint('gestorClientes', __name__)

@blueprint.get('/health')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/crear')
def crear_cliente():
    body = request.get_json()
    response = CrearCliente(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/login')
def login():
    body = request.get_json()
    response = LoginCliente(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/<cliente_id>')
def consultar_cliente(cliente_id):
    response = ConsultarCliente(cliente_id).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/')
def listar_clientes():
    response = ListarClientes().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/<cliente_id>/asignar_vendedor/<vendedor_id>')
def asignar_vendedor(cliente_id, vendedor_id):
    response = AsignarVendedor(cliente_id, vendedor_id).execute()
    return jsonify(response['response']), response['status_code'] 
