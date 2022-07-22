from typing import Dict, List

from utils import ItemJSON
from db import db


# noinspection PyUnreachableCode
class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(200))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel", back_populates="items")

    def __init__(self, title: str, description: str, price: float, store_id: int):
        self.title = title
        self.description = description
        self.price = price
        self.store_id = store_id

    @classmethod
    def find_by_id(cls, _id: int) -> "ItemModel":
        return cls.query.filter_by(id=_id).first_or_none()

    @classmethod
    def get_items(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self) -> ItemJSON:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "store_id": self.store_id,
        }
