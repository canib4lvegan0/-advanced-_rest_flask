from hmac import compare_digest

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    current_user,
    get_jwt
)
from flask_restful import Resource, reqparse

from blocklist import BLOCKLIST
from models.user import UserModel
from utils import convert_to_dec_or_alpha


def _user_parser(to):
    parser = reqparse.RequestParser()

    if to == 'post':
        parser.add_argument('username', type=str, required=True, help='Invalid cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='Invalid cannot be blank!')
        # parser.add_argument('is_admin', type=str, required=False)
    elif to == 'put':
        parser.add_argument('username', type=str, required=False)
    elif to == 'login':
        parser.add_argument('username', type=str, required=True, help='Invalid cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='Invalid cannot be blank!')

    return parser


# noinspection PyUnreachableCode
class UserRegister(Resource):
    def post(self):
        data = _user_parser('post').parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'This username already exists'}, 409

        new_user = UserModel(**data)

        try:
            new_user.save_to_db()
            return {'message': 'User created successfully.'}, 201

        except new_user.SQLAlchemyError as ex:
            return {'message': ex}, 500


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser('login').parse_args()

        if user := UserModel.find_by_username(data['username']):
            if compare_digest(user.password, data['password']):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)

                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200

        return {'message': 'Invalid credentials'}, 401

    @classmethod
    def get_user_by_id(cls, _id):
        return UserModel.find_by_id(_id)


class UserLogout(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        retrieved_jwt = get_jwt()      # jti is a "JWT ID", a unique identifier for a a JWT.
        jti = retrieved_jwt['jti']
        BLOCKLIST.add(jti)
        return {'message': 'Successfully logout'}

# noinspection PyUnreachableCode
class UserId(Resource):

    @classmethod
    def _get_user_by_param(cls, param):
        converted = convert_to_dec_or_alpha(param)

        result = None
        if type(converted) == str:
            result = UserModel.find_by_username(converted)
        elif type(converted) == int:
            result = UserModel.find_by_id(int(converted))

        if result:
            return result
        return None

    @classmethod
    @jwt_required()
    def get(cls, param):
        if user := cls._get_user_by_param(param):
            return user.to_json(), 200
        return {'message': 'User not found'}, 404

    @classmethod
    @jwt_required()
    def put(cls, param):
        if not (user := cls._get_user_by_param(param)):
            return {'message': 'User not found'}, 404

        data = _user_parser('put').parse_args()

        try:
            user.username = data['username']
            user.save_to_db()
            return {'id': user.id}, 201
        except user.SQLAlchemyError as ex:
            return {'message': ex}, 500

    @classmethod
    @jwt_required()
    def delete(cls, param):
        if not (user := cls._get_user_by_param(param)):
            return {'message': 'User not found'}, 404

        try:
            user.delete_from_db()
            return {'id': user.id}, 200
        except user.SQLAlchemyError as ex:
            return {'message': ex}, 500


class UserProfile(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        if not get_jwt_identity():
            return {'message': 'You need to be logged in to see this'}, 401

        return {
            'id': current_user.id,
            'username': current_user.username,
            'is_admin': (claims := get_jwt()) and claims['is_admin']
        }, 200


# noinspection PyUnreachableCode
class Users(Resource):

    @jwt_required()
    def get(self):
        if result := UserModel.get_users():
            users = [u.to_json() for u in result]
            return {'users': users}, 200
        else:
            return {}, 404


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        if current := get_jwt_identity():
            new_token = create_access_token(identity=current, fresh=False)
            return {'access_token': new_token}, 200

        return {'message': 'You was not logged'}, 401
