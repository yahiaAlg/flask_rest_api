from flask import Flask
from flask_smorest import Api
from resources.store import blp as StoresBlueprint
from resources.item import blp as ItemsBlueprint
import models
from db import db
import os


def create_app(db_uri: str = ""):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri or os.getenv(
        "DB_URI", "sqlite:///database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(StoresBlueprint)
    api.register_blueprint(ItemsBlueprint)
    return app
