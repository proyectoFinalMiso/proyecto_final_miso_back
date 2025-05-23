from flask import Blueprint, jsonify, request
from src.commands.crear_cliente import CrearCliente
from src.commands.consultar_cliente import ConsultarCliente
from src.commands.listar_clientes import ListarClientes
from src.commands.asignar_vendedor import AsignarVendedor
from src.commands.login_cliente import LoginCliente
from src.commands.registrar_visita import RegistrarVisita
from src.commands.listar_visitas import ListarVisitas
from src.commands.health_check import HealthCheck
from src.commands.generate_upload_url import GenerateUploadUrl
from src.commands.notify_upload_complete import NotifyUploadComplete

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

@blueprint.get('/clientes')
def listar_clientes():
    vendedor_id = request.args.get('vendedor_id')
    response = ListarClientes(vendedor_id).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/<cliente_id>/asignar_vendedor/<vendedor_id>')
def asignar_vendedor(cliente_id, vendedor_id):
    response = AsignarVendedor(cliente_id, vendedor_id).execute()
    return jsonify(response['response']), response['status_code'] 

@blueprint.post('/<cliente_id>/registrar_visita')
def registrar_visita(cliente_id):
    body = request.get_json()
    response = RegistrarVisita(cliente_id, body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/visitas')
def listar_visitas():
    cliente_id = request.args.get('cliente_id')
    vendedor_id = request.args.get('vendedor_id')
    estado = request.args.get('estado')
    sort_order = request.args.get('sort_order')

    response = ListarVisitas(
        cliente_id,
        vendedor_id,
        estado,
        sort_order
    ).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/generate_upload_url')
def generate_upload_url():
    body = request.get_json()
    response = GenerateUploadUrl(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/notify_upload_complete')
def notify_upload_complete():
    body = request.get_json()
    response = NotifyUploadComplete(body).execute()
    return jsonify(response['response']), response['status_code']
