import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.ItemModel import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="Please put a price")
    parser.add_argument('store_id', type=int, required=True, help="Every item need a store id")

    @jwt_required()
    def get(self, name):
        row = ItemModel.find_by_name(name)
        if row:
            return row.json()
        return {"message": "Item not found"}

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "Item already exists"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            ItemModel.save_to_db(item)
        except:
            return {"message": "An error occurred"}, 500

        return {"message": "Item Created successfully"}

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item Deleted!"}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return {"message": "Item updated successfully"}


class ItemList(Resource):
    def get(self):
        return [item.json() for item in ItemModel.query.all()]