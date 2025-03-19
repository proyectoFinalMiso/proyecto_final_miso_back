from flask import Blueprint, jsonify, request
from src.commands.health_check import HealthCheck

blueprint = Blueprint('productos', __name__)

@blueprint.get('/ping')
def health_check():
    return HealthCheck().execute()

