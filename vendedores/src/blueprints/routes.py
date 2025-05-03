from flask import Blueprint, jsonify, request
from src.commands.health_check import HealthCheck
from src.commands.crear_vendedor import CrearVendedor
from src.commands.obtener_vendedor import ObtenerVendedor
from src.commands.login_vendedor import LoginVendedor
from src.commands.listar_vendedores import ListarVendedores
from src.commands.plan.crear_plan import CrearPlanVentas
from src.commands.plan.listar_planes import ListarPlanes
from src.commands.plan.finalizar_plan import FinalizarPlan

blueprint = Blueprint('productos', __name__)

@blueprint.get('/ping')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/crear_vendedor')
def crear_vendedor():
    body = request.get_json()
    response = CrearVendedor(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/obtener_vendedor/<vendedor_id>')
def obtener_vendedor(vendedor_id):  
    response = ObtenerVendedor(vendedor_id).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/login')
def login():
    body = request.get_json()
    response = LoginVendedor(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/listar_vendedores')
def listar_vendedores():
    response = ListarVendedores().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/crear_plan_ventas')
def crear_plan_ventas():
    body = request.get_json()
    response = CrearPlanVentas(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/listar_planes')
def listar_planes():
    response = ListarPlanes().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/finalizar_plan')
def finalizar_plan():
    body = request.get_json()
    response = FinalizarPlan(body).execute()
    return jsonify(response['response']), response['status_code']
