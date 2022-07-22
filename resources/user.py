from hmac import compare_digest

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    current_user,
    get_jwt,
)

from sqlalchemy import exc
from flask_restful import Resource, reqparse

from blocklist import BLOCKLIST

from models.user import UserModel
from utils import to_decimal_or_alpha
import resources.resource_messages as msg


def _user_parser(to):
    parser = reqparse.RequestParser()

    if to == "post":
        parser.add_argument(
            "name", type=str, required=True, help=msg.BLANK_ERROR.format("name")
        )
        parser.add_argument(
            "username", type=str, required=True, help=msg.BLANK_ERROR.format("username")
        )
        parser.add_argument(
            "password", type=str, required=True, help=msg.BLANK_ERROR.format("password")
        )
        parser.add_argument("is_admin", type=bool, required=False, help=msg.INVALID_ERROR.format("is_admin"))
    elif to == "put":
        parser.add_argument("name", type=str, required=False)
    elif to == "login":
        parser.add_argument(
            "username", type=str, required=True, help=msg.BLANK_ERROR.format("username")
        )
        parser.add_argument(
            "password", type=str, required=True, help=msg.BLANK_ERROR.format("password")
        )

    return parser


# noinspection PyUnreachableCode
class UserRegister(Resource):

    @classmethod
    def post(cls):
        data = _user_parser("post").parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": msg.ALREADY_EXISTS.format("username")}, 409

        new_user = UserModel(**data)

        try:
            new_user.save_to_db()
            return {"message": msg.CREATED_SUCCESSFULLY.format("user")}, 201

        except RuntimeError as ex:
            return {"message": ex}, 500


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser("login").parse_args()

        if user := UserModel.find_by_username(data["username"]):
            if compare_digest(user.password, data["password"]):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200

        return {"message": msg.INVALID_ERROR.format("credential")}, 401

    @classmethod
    def get_user_by_id(cls, _id):
        return UserModel.find_by_id(_id)


class UserLogout(Resource):

    @classmethod
    @jwt_required(verify_type=False)
    def post(cls):
        jti = get_jwt()["jti"]  # jti is a "JWT ID", a unique identifier for a a JWT.
        BLOCKLIST.add(jti)
        return {"message": msg.SUCCESSFULLY.format("logout")}


# noinspection PyUnreachableCode
class UserId(Resource):

    @classmethod
    def _get_user_by_param(cls, param: str):
        converted = to_decimal_or_alpha(param)

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
    def get(cls, param: str):
        if user := cls._get_user_by_param(param):
            return user.to_json(), 200
        return {"message": "User not found"}, 404

    @classmethod
    @jwt_required()
    def put(cls, param: str):
        if not (user := cls._get_user_by_param(param)):
            return {"message": "User not found"}, 404

        data = _user_parser("put").parse_args()

        try:
            user.username = data["name"]
            user.save_to_db()
            return {"id": user.id}, 201
        except exc.SQLAlchemyError as ex:
            return {"message": ex}, 500

    @classmethod
    @jwt_required()
    def delete(cls, param: str):
        if not (user := cls._get_user_by_param(param)):
            return {"message": "User not found"}, 404

        try:
            user.delete_from_db()
            return {"id": user.id}, 200
        except user.SQLAlchemyError as ex:
            return {"message": ex}, 500


class UserProfile(Resource):

    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        if not get_jwt_identity():
            return {"message": msg.NOT_ADMIN}, 401

        return {
            "id": current_user.id,
            "name": current_user.name,
            "username": current_user.username,
            "is_admin": current_user.is_admin,
        }, 200


# noinspection PyUnreachableCode
class Users(Resource):

    @classmethod
    @jwt_required()
    def get(cls):
        if result := UserModel.get_users():
            users = [u.to_json() for u in result]
            return {"users": users}, 200


class UserAdmin:

    @classmethod
    def get_is_admin(cls, _id: int):
        user = UserModel.find_by_id(_id)
        return user.is_admin if user else False


class RefreshToken(Resource):

    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        if current := get_jwt_identity():
            new_token = create_access_token(identity=current, fresh=False)
            return {"access_token": new_token}, 200

        return {"message": msg.NEED_LOGGED_IN}, 401
