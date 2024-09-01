import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import StoreSchema, StoreUpdateSchema
from models import StoreModel
from db import db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self):
        store_data = request.get_json()
        store_id = store_data["id"]
        store = StoreModel.query.get_or_404(store_id)
        return store

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data: dict):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
            return store, 201
        except IntegrityError:
            abort(400, message="Store already exists")
        except SQLAlchemyError:
            abort(400, message="An error occurred while creating the store")

    @blp.arguments(StoreUpdateSchema)
    @blp.response(201, StoreSchema)
    def put(self, store_data: dict):
        store_id = store_data.get(id)
        new_store = StoreModel.query.get(store_id)
        try:
            if new_store:
                for key in new_store:
                    setattr(new_store, key, store_data.get(key))

            else:
                new_store = StoreModel(**store_data)
                db.session.add(new_store)

            db.session.commit()
            return new_store

        except SQLAlchemyError:
            db.session.rollback()
            abort(400, message="An error occurred while updating the item")

    def delete(self):
        store_id = request.json["id"]  # type: ignore
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(400, message="An error occurred while deleting the store")


@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
