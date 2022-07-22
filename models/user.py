from typing import List

from utils import UserJSON
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, name: str, username: str, password: str, is_admin: bool = False):
        self.name = name
        self.username = username
        self.password = password
        self.is_admin = is_admin

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).one_or_none()

    @classmethod
    def get_users(cls) -> List["UserModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self) -> UserJSON:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "is_admin": self.is_admin,
        }
