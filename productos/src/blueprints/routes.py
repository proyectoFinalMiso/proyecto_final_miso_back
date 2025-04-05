from flask import Blueprint, jsonify, request
from src.commands.listar_fabricantes import ListarFabricantes
from src.commands.crear_fabricante import CrearFabricante
from src.commands.buscar_fabricante import BuscarFabricante
from src.commands.listar_productos import ListarProductos
from src.commands.crear_producto import CrearProducto
from src.commands.buscar_producto import BuscadorProducto
from src.commands.health_check import HealthCheck
from src.commands.procesar_archivo_productos import ProcesarArchivoProductos
from src.commands.crear_producto_masivo import CrearProductoMasivo

blueprint = Blueprint('productos', __name__)

@blueprint.get('/ping')
def health_check():
    return HealthCheck().execute()

@blueprint.post('/crear_fabricante')
def crear_fabricante():
    body = request.get_json()
    response = CrearFabricante(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/crear_producto')
def crear_producto():
    body = request.get_json()
    response = CrearProducto(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/crear_producto/masivo')
def crear_producto_masivo():
    if 'archivo' not in request.files:
        return jsonify({"response": {"msg": "Ha ocurrido un error al procesar el archivo"}}), 500
    
    archivo = request.files['file']
    nombre_archivo = archivo.filename.lower()
    productos = ProcesarArchivoProductos(archivo, nombre_archivo).execute()
    response = CrearProductoMasivo(productos).execute()
    return jsonify(response['response']), response['status_code']
                       
@blueprint.post('/buscar_producto')
def buscar_producto():
    body = request.get_json()
    response = BuscadorProducto(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.post('/buscar_fabricante')
def buscar_fabricante():
    body = request.get_json()
    response = BuscarFabricante(body).execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/listar_fabricantes')
def listar_fabricantes():
    response = ListarFabricantes().execute()
    return jsonify(response['response']), response['status_code']

@blueprint.get('/listar_productos')
def listar_productos():
    response = ListarProductos().execute()
    return jsonify(response['response']), response['status_code']