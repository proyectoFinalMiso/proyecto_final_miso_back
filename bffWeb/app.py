from sys import argv

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from src.blueprints.routes import blueprint
from waitress import serve

load_dotenv('.env')
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(blueprint)

if __name__ == '__main__':

    if argv[1] == 'dev':
        app.run(debug=True, host="0.0.0.0", port=3097)
    else:
        serve(app, host="0.0.0.0", port=3097, threads=8, connection_limit=400)
