import requests
from os import getenv
from flask import Blueprint, jsonify, request

blueprint = Blueprint('bffWeb', __name__)

MS_PRODUCTOS_URL = rf"{getenv('MS_PRODUCTOS_URL')}"
MS_PEDIDOS_URL = rf"{getenv('MS_PEDIDOS_URL')}"

def handle_requests(host, path):
    url = f"{host}/{path}"
    if request.method != "GET":
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json(),
        )
        return response
    response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != "Host"},
        )
    return response

@blueprint.get("/")
def health_check():
    return jsonify({"msg": 'La API del cliente web se encuentra operativa'}), 200

@blueprint.route("/api/productos/<path:path>", methods=["GET", "POST"])
def proxy_ms_productos(path=None):
    response = handle_requests(MS_PRODUCTOS_URL, path)
    return jsonify(response.json()), response.status_code

@blueprint.route("/api/gestorPedidos/<path:path>", methods=["GET", "POST"])
def proxy_ms_pedidos(path=None):
    response = handle_requests(MS_PEDIDOS_URL, path)
    return jsonify(response.json()), response.status_code