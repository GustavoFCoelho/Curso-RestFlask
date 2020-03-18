from flask_jwt import jwt_required
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, \
    get_raw_jwt
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.UserModel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.findByUsername(data['username']):
            return {'message': "User already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.findById(user_id)
        if not user:
            return {"message": "User Not Found"}

        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.findById(user_id)
        if not user:
            return {"message": "User Not Found"}
        user.delete_from_db()
        return {"message": "User Deleted"}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.findByUsername(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        return {'message': "Invalid Credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully Logged out'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}
