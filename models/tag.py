from db import db


class TagModel(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags", lazy=True)
    items = db.relationship(
        "ItemModel", back_populates="tags", lazy=True, secondary="items_tags"
    )

    def __repr__(self):
        return f"TagModel(name={self.name}, store_id={self.store_id})"
