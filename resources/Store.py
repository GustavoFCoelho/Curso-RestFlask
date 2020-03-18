from flask_restful import Resource

from models.StoreModel import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {"message": "Store not found"}

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "This store already exists"}
        try:
            StoreModel(name).save_to_db()
        except:
            return {"message": "Internal server error has occurred"}

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()

        return  {"message": "Store Deleted"}

class StoreList(Resource):
    def get(self):
        return [store.json() for store in StoreModel.query.all()]