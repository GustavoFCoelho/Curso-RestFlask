from werkzeug.security import safe_str_cmp

from models.UserModel import UserModel


def authenticate(username, password):
    user = UserModel.findByUsername(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.findById(user_id)
