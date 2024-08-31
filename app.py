from pprint import pprint
import uuid
from flask import Flask, request

app = Flask(__name__)

stores = {}
items = {}


@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


# @app.post("/store")
# def create_store():
#     new_store: dict = request.get_json()
#     pprint(new_store)
#     new_store.update({"items": []})
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
#             return {"message": "Store not found"}, 404


# @app.get("/store/<string:name>")
# def get_store(name: str):
#     for store in stores:
#         if store["name"] == name:
#             return store, 200
#     return {"message": "Store not found"}, 404


# @app.get("/store/<string:name>/item")
# def get_item_in_store(name: str):
#     for store in stores:
#         if store["name"] == name:
#             return {"items": store["items"]}, 200
#     return {"message": "Store not found"}, 404


@app.get("/store")
def get_store():
    store_data = request.get_json()
    store_id = store_data["id"]
    if store_id in stores:
        return {"store": stores[store_id]}
    return {"message": f"no store with an id of {store_id}"}, 404


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return {"store": new_store}, 201


@app.get("/items")
def get_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return {"item": items[item_id]}
    except KeyError:
        return {"message": "item not found"}, 404


@app.put("/store")
def update_store(store_id):
    store_id = request.json["store_id"]
    if store_id not in stores:
        return ({"message": f"no such a store with an id of {store_id}"}, 404)
    required_fields = ["name", "address"]
    store_data = request.get_json()
    if not all(field in store_data for field in required_fields):
        return {"message": "missing required fields"}, 400
    stores[store_id] |= store_data
    return {"store": stores[store_id]}, 201


@app.delete("/store")
def delete_store():
    store_id = request.json["store_id"]
    if store_id not in stores:
        return ({"message": f"no such a store with an id of {store_id}"},)
    del stores[store_id]
    return {"message": f"store with id {store_id} has been deleted"}, 200


@app.post("/item")
def create_items():
    item_data = request.get_json()
    store_id = item_data["store_id"]
    if store_id not in stores:
        return {"message": f"no such a store with an id of {store_id}"}, 404
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return {"item": new_item}, 201


@app.put("/item/<string:id>")
def update_item(id):
    if id not in items:
        return {"message": f"no item with an id of {id}"}, 404
    required_fields = [
        "name",
        "price",
        "store_id",
        "description",
        "category",
    ]
    item_data = request.get_json()
    if not all(field in item_data for field in required_fields):
        return {"message": "missing required fields"}, 400
    items[id] |= item_data
    return {"item": items[id]}, 201


@app.delete("/item/<string:id>")
def delete_item(id):
    if id not in items:
        return {"message": f"no item with an id of {id}"}, 404
    del items[id]
    return {"message": f"item with id {id} has been deleted"}, 200
