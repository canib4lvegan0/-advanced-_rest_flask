import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db

from blocklist import BLOCKLIST

from resources.aline import Aline
from resources.home import Home
from resources.item import ItemRegister, Items, ItemId
from resources.store import StoreRegister, StoreId, Stores
from resources.user import (
    UserRegister,
    UserLogin,
    UserLogout,
    Users,
    UserId,
    UserProfile,
    RefreshToken
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'robsu'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 600  # seconds

api = Api(app)
jwt = JWTManager(app)  # /not creating auth endpoint


@jwt.user_identity_loader
def user_identity_lookup(identify):
    return identify


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserLogin.get_user_by_id(_id=identity)


@jwt.additional_claims_loader
def add_claims_to_jwt(identify):
    if identify == int(os.environ.get('ADMIN', '1')):
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expire_token_callback(jwt_header, jwt_payload):
    return {'message': 'The token has expired', 'error': 'expired_token'}, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {'message': error, 'error': 'invalid_token'}, 401


@jwt.unauthorized_loader
def unauthorized_token_callback(error):
    return {'message': error, 'error': 'unauthorized_token'}, 401


@jwt.needs_fresh_token_loader
def needs_refresh_token_callback(jwt_header, jwt_payload):
    return {'message': 'You need refresh your token', 'error': 'unrefreshed_token'}, 401


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return {'message': 'The token has been revoked'}, 401


api.add_resource(ItemRegister, '/item_register', methods=['POST'])
api.add_resource(ItemId, '/item/<int:_id>', methods=['GET', 'PUT', 'DELETE'])
api.add_resource(Items, '/items', methods=['GET'])
api.add_resource(UserRegister, '/user_register', methods=['POST'])
api.add_resource(UserLogin, '/login', methods=['POST'])
api.add_resource(UserLogout, '/logout', methods=['POST'])
api.add_resource(RefreshToken, '/refresh_token', methods=['POST'])
api.add_resource(UserId, '/user/<param>', methods=['GET', 'PUT', 'DELETE'])
api.add_resource(Users, '/users', methods=['GET'])
api.add_resource(UserProfile, '/my_profile', methods=['GET'])
api.add_resource(StoreRegister, '/store_register', methods=['POST'])
api.add_resource(StoreId, '/store/<int:_id>', methods=['GET', 'PUT', 'DELETE'])
api.add_resource(Stores, '/stores', methods=['GET'])

api.add_resource(Aline, '/aline', methods=['GET'])
api.add_resource(Home, '/', methods=['GET'])


if os.environ.get('CREATE_TABLES') == 'True':
    import run
    print('Running on mode creating tables...')
    run.init(app=app, db=db)
else:
    db.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
