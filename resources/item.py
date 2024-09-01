import logging
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, id):
        item = ItemModel.query.get_or_404(id)
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data: dict, id: str):
        item = ItemModel.query.get(id)
        try:
            if item:
                for key in item_data:
                    setattr(item, key, item_data.get(key))
            else:
                item = ItemModel(id=id, **item_data)  # type: ignore
                db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError:
            db.session.rollback()
            abort(400, message="An error occurred while updating the item")

    def delete(self, id):
        retrieved_item = ItemModel.query.get_or_404(id)
        try:
            db.session.delete(retrieved_item)
            db.session.commit()
            return {"message": "Item deleted"}, 200
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "An error occurred"}, 500


@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data: dict):
        new_item = ItemModel(**item_data)
        try:
            db.session.add(new_item)
            db.session.commit()
            return new_item
        except IntegrityError:
            return abort(400, message="item already exists")
        except SQLAlchemyError:
            return abort(500, message="database error")
