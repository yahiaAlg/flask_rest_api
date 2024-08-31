import uuid
from flask import Flask, request
from flask_smorest import abort

app = Flask(__name__)

stores = {}
items = {}


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
@app.get("/stores")
def get_stores():
    return list(stores.values())


@app.get("/store")
def get_store():
    store_data = request.get_json()
    store_id = store_data["store_id"]
    if store_id in stores:
        return stores[store_id]
    return abort(404, message=f"no store with an id of {store_id}")


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "store_id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.put("/store")
def update_store():
    store_id = request.json["store_id"]
    if store_id not in stores:
        return abort(404, message=f"no such a store with an id of {store_id}")
    required_fields = ["name", "store_id"]
    store_data = request.get_json()
    if not all(field in store_data for field in required_fields):
        return abort(400, message="missing required fields")
    stores[store_id] |= store_data
    return stores[store_id], 201


@app.delete("/store")
def delete_store():
    store_id = request.json["store_id"]
    if store_id not in stores:
        return abort(404, f"no such a store with an id of {store_id}")
    del stores[store_id]
    return f"store with id {store_id} has been deleted", 200


@app.get("/items")
def get_items():
    return list(items.values())


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return abort(404, message="item not found")


@app.post("/item")
def create_item():
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


@app.put("/item/<string:id>")
def update_item(id):
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


@app.delete("/item/<string:id>")
def delete_item(id):
    if id not in items:
        return abort(404, message=f"no item with an id of {id}")
    del items[id]
    return f"item with id {id} has been deleted", 200
