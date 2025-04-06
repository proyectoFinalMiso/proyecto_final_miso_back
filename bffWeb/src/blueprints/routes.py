import requests
from os import getenv
from flask import Blueprint, jsonify, request

blueprint = Blueprint('bffWeb', __name__)

MS_PRODUCTOS_URL = rf"{getenv('MS_PRODUCTOS_URL')}"
MS_PEDIDOS_URL = rf"{getenv('MS_PEDIDOS_URL')}"
MS_VENDEDOR_URL = rf"{getenv('MS_VENDEDOR_URL')}"
MS_GESTOR_CLIENTES_URL = rf"{getenv('MS_GESTOR_CLIENTES_URL')}"

def handle_requests(host, path):
    url = f"{host}/{path}"
    headers = {key: value for key, value in request.headers if key != ["Host"]}

    if request.method != "GET":

        if request.content_type and request.content_type.startswith('multipart/form-data'):
            headers.pop("Content-Type", None)
            files = {key: (file.filename, file.stream, file.mimetype) for key, file in request.files.items()}
            data = request.form.to_dict()

            response = requests.request(
                method=request.method,
                url=url,
                headers=headers,
                data=data,
                files=files
            )
        else:
            response = requests.request(
                method=request.method,
                url=url,
                headers=headers,
                json=request.get_json(),
            )
        return response
    
    response = requests.request(
            method=request.method,
            url=url,
            headers=headers
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

@blueprint.route("/api/vendedor/<path:path>", methods=["GET", "POST"])
def proxy_ms_vendedores(path=None):
    response = handle_requests(MS_VENDEDOR_URL, path)
    return jsonify(response.json()), response.status_code