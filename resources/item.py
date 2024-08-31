import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message="item not found")

    def post(self, item_id):
        required_fields = [
            "name",
            "price",
            "store_id",
            "description",
            "category",
        ]
        item_data = request.get_json()
        if not all(field in item_data for field in required_fields):
            return abort(400, massage="missing required fields")
        store_id = item_data["store_id"]
        if store_id not in stores:
            return abort(404, message=f"no such a store with an id of {store_id}")
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "item_id": item_id}
        items[item_id] = new_item
        return new_item, 201

    def put(self, item_id):
        if id not in items:
            return abort(404, message=f"no item with an id of {id}")
        permitted_fields = [
            "name",
            "price",
            "store_id",
            "description",
            "category",
        ]
        item_data = request.get_json()
        if not all(field in permitted_fields for field in item_data):
            return abort(400, message="not permitted fields")
        items[id] |= item_data
        return items[id], 201

    def delete(self, item_id):
        if id not in items:
            return abort(404, message=f"no item with an id of {id}")
        del items[id]
        return f"item with id {id} has been deleted", 200


@blp.route("/items")
class ItemList(MethodView):
    def get(self):
        return list(items.values())
