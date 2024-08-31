import uuid
from flask import Flask, request
from flask_smorest import abort

app = Flask(__name__)


# @app.post("/store")
# def create_store():
#     new_store: dict = request.get_json()
#     pprint(new_store)
#     new_store.update({items": [])
#     stores.append(new_store)
#     return stores, 201


# @app.post("/store/<string:name>/item")
# def create_item(name: str):
#     new_item: dict = request.get_json()
#     for store in stores:
#         if store["name"] == name:
#             store["items"].append(new_item)
#             return store, 201
#         else:
# abort(404,            return "Store not found")


# @app.get("/store/<string:name>")
# def get_store(name: str):
#     for store in stores:
#         if store["name"] == name:
#             return store, 200
# abort(404,    return "Store not found")


# @app.get("/store/<string:name>/item")
# def get_item_in_store(name: str):
#     for store in stores:
#         if store["name"] == name:
#             return store["items"], 200
# abort(404,    return "Store not found")
from db import stores, items
from flask import Flask
from flask_smorest import abort, Api


app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Store API"
app.config["API_VERSION"] = "v1.0"
app.config["OPENAPI_VERSION"] = "3.0.2"

app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAIPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app = Api(app)
app.register_blueprint()
