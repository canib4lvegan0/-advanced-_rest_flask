from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models.item import ItemModel


def _item_parser(to):
    parser = reqparse.RequestParser()
    if to == 'post':
        parser.add_argument('title', type=str, required=True, help="Title cannot be blank.")
        parser.add_argument('description', type=str, required=False, help="Description invalid.")
        parser.add_argument('price', type=float, required=True, help="Price cannot be blank.")
        parser.add_argument('store_id', type=int, required=True, help="Every item needs a store_id.")

    if to == 'put':
        parser.add_argument('title', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('price', type=float, required=False)
        parser.add_argument('store_id', type=int, required=False)

    return parser


# noinspection PyUnreachableCode
class ItemRegister(Resource):
    @jwt_required(refresh=True)
    def post(self):
        if not get_jwt_identity():
            return {'message': 'You need to be logged in to see this'}, 401

        if (claims := get_jwt()) and not claims['is_admin']:
            return {'message': 'You are not admin. You can not do this.'}

        data = _item_parser('post').parse_args()
        new_item = ItemModel(**data)

        try:
            new_item.save_to_db()
            return {'message': 'Item created successfully.'}, 201
        except SQLAlchemyError as ex:
            return {'message': ex.__str__()}, 500


# noinspection PyUnreachableCode
class ItemId(Resource):
    def get(self, _id):
        if result := ItemModel.find_by_id(_id):
            return {'item': result.to_json()}

    @jwt_required(refresh=True)
    def put(self, _id):
        if (claims := get_jwt()) and not claims['is_admin']:
            return {'message': 'You are not admin. You can not do this.'}

        data = _item_parser('put').parse_args()

        if result := ItemModel.find_by_id(_id):
            result.title = data['title']
            result.description = data['description']
            result.price = data['price']
            result.price = data['store_id']

            result.save_to_db()

            return {'id': result.id}, 201
        else:
            return {'message': 'Item not found'}, 404

    @jwt_required(refresh=True)
    def delete(self, _id):
        if (claims := get_jwt()) and not claims['is_admin']:
            return {'message': 'You are not admin. You can not do this.'}

        if result := ItemModel.find_by_id(_id):
            result.delete_from_db()
            return {'id': result.id}, 200

        return {'message': 'Item not found'}, 404


# noinspection PyUnreachableCode
class Items(Resource):
    def get(self):
        if result := ItemModel.get_items():
            items = [i.to_json() for i in result]
            return {'items': items}, 200
        else:
            return {}, 404
