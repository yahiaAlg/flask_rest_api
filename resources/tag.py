import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, TagUpdateSchema
from models import TagModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/tag/<string:id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
        tag = TagModel.query.get_or_404(id)
        return tag

    @blp.arguments(TagUpdateSchema)
    @blp.response(201, TagSchema)
    def put(self, tag_data: dict, id: str):
        tag = TagModel.query.get(id)
        if (
            tag_data.get("store_id")
            and TagModel.query.filter(TagModel.store_id == tag_data["store_id"]).count()
            > 0
        ):
            if (
                tag_data.get("name")
                and TagModel.query.filter(TagModel.name == tag_data["name"]).count() > 0
            ):
                return abort(
                    400,
                    message=f"Tag already exists in the store with the id: {tag_data['store_id']}",
                )
        try:
            if tag:
                for key in tag_data:
                    setattr(tag, key, tag_data.get(key))
            else:
                tag = TagModel(id=id, **tag_data)  # type: ignore
                db.session.add(tag)
            db.session.commit()
            return tag
        except SQLAlchemyError:
            db.session.rollback()
            abort(400, message="An error occurred while updating the tag")

    def delete(self, id):
        retrieved_tag = TagModel.query.get_or_404(id)
        try:
            if retrieved_tag.items:
                for item in retrieved_tag.items:
                    item.tags.remove(retrieved_tag)
                    db.session.add(item)
                    logging.info(f" Tag {id} removed from item {item.id}")

            db.session.delete(retrieved_tag)
            db.session.commit()
            return {
                "message": f"Tag {retrieved_tag} located in the store {retrieved_tag.store_id} has been deleted "
            }, 200

        except SQLAlchemyError:
            db.session.rollback()
            return abort(500, message="An error occurred")


@blp.route("/tags")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data: dict):
        if (
            tag_data.get("store_id")
            and TagModel.query.filter(TagModel.store_id == tag_data["store_id"]).count()
            > 0
        ):
            if (
                tag_data.get("name")
                and TagModel.query.filter(TagModel.name == tag_data["name"]).count() > 0
            ):
                return abort(
                    400,
                    message=f"Tag already exists in the store with the id: {tag_data['store_id']}",
                )

        new_tag = TagModel(**tag_data)
        try:
            db.session.add(new_tag)
            db.session.commit()
            return new_tag
        except SQLAlchemyError:
            return abort(500, message="database error")


@blp.route("/store/<string:store_id>/tags")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id: str):
        return TagModel.query.filter_by(store_id=store_id).all()
