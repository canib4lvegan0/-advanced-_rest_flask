
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse
from models.store import StoreModel


def _store_parser(to):
    parser = reqparse.RequestParser()
    if to == 'post':
        parser.add_argument('title', type=str, required=True, help="Title cannot be blank.")

    if to == 'put':
        parser.add_argument('title', type=str, required=False)

    return parser


# noinspection PyUnreachableCode
class StoreRegister(Resource):

    @jwt_required()
    def post(self):
        if (claims := get_jwt()) and not claims['is_admin']:
            return {'message': 'You are not admin. You can not do this.'}

        data = _store_parser('post').parse_args()
        new_store = StoreModel(**data)

        try:
            new_store.save_to_db()
            return {'message': 'Store created successfully.'}, 201

        except new_store.SQLAlchemyError as ex:
            return {'message': ex}, 500


# noinspection PyUnreachableCode
class StoreId(Resource):
    def get(self, _id):
        if result := StoreModel.find_by_id(_id):
            return {'item': result.to_json()}

    @jwt_required()
    def put(self, _id):
        if (claims := get_jwt()) and not claims['is_admin']:
            return {'message': 'You are not admin. You can not do this.'}

        data = _store_parser('put').parse_args()

        if result := StoreModel.find_by_id(_id):
            result.title = data['title']

            result.save_to_db()

            return {'id': result.id}, 201
        else:
            return {'message': 'Store not found'}, 404

    @jwt_required()
    def delete(self, _id):
        if (claims := get_jwt()) and not claims['is_admin']:
            return {'message': 'You are not admin. You can not do this.'}

        if result := StoreModel.find_by_id(_id):
            result.delete_from_db()
            return {'id': result.id}, 200

        return {'message': 'Store not found'}, 404


# noinspection PyUnreachableCode
class Stores(Resource):
    def get(self):

        if result := StoreModel.get_stores():
            items = [i.to_json() for i in result]
            return {'stores': items}, 200
        else:
            return {}, 404
