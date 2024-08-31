import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    def get(self):
        store_data = request.get_json()
        store_id = store_data["store_id"]
        if store_id in stores:
            return stores[store_id]
        return abort(404, message=f"no store with an id of {store_id}")

    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "store_id": store_id}
        stores[store_id] = new_store
        return new_store, 201

    def put(self):
        store_id = request.json["store_id"]
        if store_id not in stores:
            return abort(404, message=f"no such a store with an id of {store_id}")
        required_fields = ["name", "store_id"]
        store_data = request.get_json()
        if not all(field in store_data for field in required_fields):
            return abort(400, message="missing required fields")
        stores[store_id] |= store_data
        return stores[store_id], 201

    def delete(self):
        store_id = request.json["store_id"]
        if store_id not in stores:
            return abort(404, f"no such a store with an id of {store_id}")
        del stores[store_id]
        return f"store with id {store_id} has been deleted", 200


@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        return list(stores.values())
