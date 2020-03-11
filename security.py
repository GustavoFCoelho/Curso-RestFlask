from werkzeug.security import safe_str_cmp

from model.User import User

users = {
    User(1, 'bob', 'asd')
}

user_mapping = {u.username: u for u in users}

user_mapping_id = {u.id: u for u in users}


def authenticate(username, password):
    user = user_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_mapping_id.get(user_id, None)
