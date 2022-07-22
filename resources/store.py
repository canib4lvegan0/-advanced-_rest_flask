from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse

from models.store import StoreModel
import resources.resource_messages as msg

def _store_parser(to):
    parser = reqparse.RequestParser()
    if to == "post":
        parser.add_argument(
            "title", type=str, required=True, help=msg.BLANK_ERROR.format("title")
        )

    if to == "put":
        parser.add_argument("title", type=str, required=False, help=msg.INVALID_ERROR.format("title"))

    return parser


# noinspection PyUnreachableCode
class StoreRegister(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        if (claims := get_jwt()) and not claims["is_admin"]:
            return {"message": msg.NOT_ADMIN}

        data = _store_parser("post").parse_args()
        new_store = StoreModel(**data)

        try:
            new_store.save_to_db()
            return {"message": msg.CREATED_SUCCESSFULLY.format("store")}, 201

        except new_store.SQLAlchemyError as ex:
            return {"message": ex}, 500


# noinspection PyUnreachableCode
class StoreId(Resource):

    @classmethod
    def get(cls, _id):
        if result := StoreModel.find_by_id(_id):
            return {"item": result.to_json()}

    @classmethod
    @jwt_required()
    def put(cls, _id):
        if (claims := get_jwt()) and not claims["is_admin"]:
            return {"message": msg.NOT_ADMIN}

        data = _store_parser("put").parse_args()

        if result := StoreModel.find_by_id(_id):
            result.title = data["title"]

            result.save_to_db()

            return {"id": result.id}, 201
        else:
            return {"message": msg.NOT_FOUND.format("store")}, 404

    @classmethod
    @jwt_required()
    def delete(cls, _id):
        if (claims := get_jwt()) and not claims["is_admin"]:
            return {"message": msg.NOT_ADMIN}

        if result := StoreModel.find_by_id(_id):
            result.delete_from_db()
            return {"id": result.id}, 200

        return {"message": msg.NOT_FOUND}, 404


# noinspection PyUnreachableCode
class Stores(Resource):

    @classmethod
    def get(cls):
        if result := StoreModel.get_stores():
            items = [i.to_json() for i in result]
            return {"stores": items}, 200
