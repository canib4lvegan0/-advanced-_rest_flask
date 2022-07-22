from typing import Dict, List

from utils import StoreJSON
from db import db


# noinspection PyUnreachableCode
class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, title: str):
        self.title = title

    @classmethod
    def find_by_id(cls, _id) -> "StoreModel":
        return cls.query.filter_by(id=_id).one_or_none()

    @classmethod
    def get_stores(cls) -> List["StoreModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self) -> StoreJSON:
        return {
            "id": self.id,
            "title": self.title,
            "items": [i.to_json() for i in self.items],
        }
