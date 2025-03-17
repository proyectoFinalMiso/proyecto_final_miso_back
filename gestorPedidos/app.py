from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from sys import argv
from waitress import serve

from src.blueprints.routes import blueprint
from src.constants.urls import database_host
from src.models.model import db

load_dotenv('.env')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(blueprint)

def config_app(db_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    with app.app_context():
        db.init_app(app)
        db.create_all()

if __name__ == '__main__':
    db_url = database_host()
    config_app(db_url)
    
    if argv[1] == 'dev':        
        app.run(debug=True, host="0.0.0.0", port=3002)
    else:
        serve(app, host="0.0.0.0", port=3002)
    
