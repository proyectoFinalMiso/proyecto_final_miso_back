import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from os import getenv
from sys import argv
from waitress import serve
from sqlalchemy import create_engine

from src.blueprints.routes import blueprint
from src.constants.urls import database_host
from src.models.model import db


app = Flask(__name__)
app.register_blueprint(blueprint)

def config_app(db_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    with app.app_context():
        db.init_app(app)
        db.create_all()

if __name__ == '__main__':
    try:
        if argv[1] == "dev":
            load_dotenv(".env.test")

            DB_USER = os.environ.get('DB_USER')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            DB_HOST = os.environ.get('DB_HOST')
            DB_PORT = os.environ.get('DB_PORT')
            DB_NAME = os.environ.get('DB_NAME')
            
            db_url = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            config_app(db_url)
            app.run(host="0.0.0.0", port=3005, debug=True)

        else:
            load_dotenv(".env.production")

            DB_USER = os.environ.get('DB_USER')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            DB_HOST = os.environ.get('DB_HOST')
            DB_PORT = os.environ.get('DB_PORT')
            DB_NAME = os.environ.get('DB_NAME')
            
            db_url = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

            print(db_url)
            
            config_app(db_url)
            serve(app, host="0.0.0.0", port=3005, threads=2)
            # print('bad command')

    except IndexError:
        load_dotenv(".env.production")
        serve(app, host="0.0.0.0", port=3005, threads=2)