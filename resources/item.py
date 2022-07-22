from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models.item import ItemModel
import resources.resource_messages as msg


def _item_parser(to):
    parser = reqparse.RequestParser()
    if to == "post":
        parser.add_argument(
            "title", type=str, required=True, help=msg.BLANK_ERROR.format("title")
        )
        parser.add_argument(
            "description", type=str, required=True, elp=msg.BLANK_ERROR.format("description")
        )
        parser.add_argument(
            "price", type=float, required=True, help=msg.BLANK_ERROR.format("price")
        )
        parser.add_argument(
            "store_id", type=int, required=True, help=msg.BLANK_ERROR.format("store_id")
        )
    elif to == "put":
        parser.add_argument("title", type=str, required=False, help=msg.INVALID_ERROR.format("title"))
        parser.add_argument("description", type=str, required=False, help=msg.INVALID_ERROR.format("description"))
        parser.add_argument("price", type=float, required=False, help=msg.INVALID_ERROR.format("price"))
        parser.add_argument("store_id", type=int, required=False, help=msg.INVALID_ERROR.format("store_id"))

    return parser


# noinspection PyUnreachableCode
class ItemRegister(Resource):

    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        if not get_jwt_identity():
            return {"message": msg.NEED_LOGGED_IN}, 401
        if (claims := get_jwt()) and not claims["is_admin"]:
            return {"message": msg.NOT_ADMIN}

        data = _item_parser("post").parse_args()
        new_item = ItemModel(**data)

        try:
            new_item.save_to_db()
            return {"message": msg.CREATED_SUCCESSFULLY.format("item")}, 201
        except SQLAlchemyError as ex:
            return {"message": ex.__str__()}, 500


# noinspection PyUnreachableCode
class ItemId(Resource):

    @classmethod
    def get(cls, _id: int):
        if result := ItemModel.find_by_id(_id):
            return {"item": result.to_json()}

    @classmethod
    @jwt_required(refresh=True)
    def put(cls, _id: int):
        if (claims := get_jwt()) and not claims["is_admin"]:
            return {"message": msg.NOT_ADMIN}

        data = _item_parser("put").parse_args()

        if result := ItemModel.find_by_id(_id):
            result.title = data["title"]
            result.description = data["description"]
            result.price = data["price"]
            result.price = data["store_id"]

            result.save_to_db()

            return {"id": result.id}, 201
        else:
            return {"message": msg.NOT_FOUND.format("item")}, 404

    @classmethod
    @jwt_required(refresh=True)
    def delete(cls, _id: int):
        if (claims := get_jwt()) and not claims["is_admin"]:
            return {"message": msg.NOT_ADMIN}

        if result := ItemModel.find_by_id(_id):
            result.delete_from_db()
            return {"id": result.id}, 200

        return {"message": msg.NOT_FOUND.format("item")}, 404


# noinspection PyUnreachableCode
class Items(Resource):

    @classmethod
    def get(cls):
        if result := ItemModel.get_items():
            items = [i.to_json() for i in result]
            return {"items": items}, 200
