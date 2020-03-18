from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.Item import Item, ItemList
from resources.Store import Store, StoreList
from resources.User import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret"
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/user')
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run()
