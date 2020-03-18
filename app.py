from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from resources.Item import Item, ItemList
from resources.Store import Store, StoreList
from resources.User import UserRegister, User, UserLogin, TokenRefresh, UserLogout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLE'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = "secret"
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/user')
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, '/token')
api.add_resource(UserLogout, '/logout')


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_blacklist(decryted_token):
    return decryted_token['jti'] in BLACKLIST


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The Token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid():
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized():
    return jsonify({
        'description': 'Unauthorized access',
        'error': 'token_expired'
    }), 401


@jwt.needs_fresh_token_loader
def fresh_token():
    return jsonify({
        'description': 'The Token as not fresh',
        'error': 'fresh_token'
    }), 401


@jwt.revoked_token_loader
def revoke():
    return jsonify({
        'description': 'The Token has been revoked',
        'error': 'token_revoked'
    }), 401


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run()
