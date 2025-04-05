from flask import Flask
from flask_cors import CORS
from sys import argv
from waitress import serve

from src.blueprints.routes import blueprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(blueprint)

if __name__ == '__main__':
    
    if argv[1] == 'dev':        
        app.run(debug=True, host="0.0.0.0", port=3096)
    else:
        serve(app, host="0.0.0.0", port=3096, threads=8, connection_limit=400)
