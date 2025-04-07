import os
from dotenv import load_dotenv
from flask import Flask
from sys import argv
from waitress import serve

from src.blueprints.routes import blueprint
from src.models.model import db

load_dotenv('.env')

app = Flask(__name__)

app.register_blueprint(blueprint)

def config_app(db_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    with app.app_context():
        db.init_app(app)
        db.create_all()

if __name__ == "__main__":
    try:
        if argv[1] == "dev":
            load_dotenv(".env.test")

            DB_USER = os.environ.get("DB_USER")
            DB_PWD = os.environ.get("DB_PWD")
            DB_HOST = os.environ.get("DB_HOST")
            DB_PORT = os.environ.get("DB_PORT")
            DB_NAME = os.environ.get("DB_NAME")

            db_url = f"postgresql+pg8000://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}"
            config_app(db_url)
            app.run(host="0.0.0.0", port=3006, debug=True)

        else:
            load_dotenv(".env.production")

            DB_USER = os.environ.get("DB_USER")
            DB_PWD = os.environ.get("DB_PWD")
            DB_HOST = os.environ.get("DB_HOST")
            DB_PORT = os.environ.get("DB_PORT")
            DB_NAME = os.environ.get("DB_NAME")

            db_url = f"postgresql+pg8000://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}"

            print(db_url)

            config_app(db_url)
            serve(app, host="0.0.0.0", port=3006, threads=2)
            print("bad command")

    except IndexError:
        load_dotenv(".env.production")
        serve(app, host="0.0.0.0", port=3006, threads=2)
