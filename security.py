from werkzeug.security import safe_str_cmp

from models.UserModel import UserModel

users = {
    UserModel(1, 'bob', 'asd')
}

user_mapping = {u.username: u for u in users}

user_mapping_id = {u.id: u for u in users}


def authenticate(username, password):
    user = UserModel.findByUsername(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.findById(user_id)
