from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        "name": 'My Wonderful Store',
        "items": [
            {
                "name": "My Item",
                "price": 15.99
            }
        ]
    }
]


@app.route("/store", methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data['name'],
        "items": []
    }
    stores.append(new_store)
    return jsonify(stores)


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({"message": "Store Not Found"})


@app.route('/store')
def get_stores():
    return jsonify(stores)


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"message": "Store Not Found"})


@app.route("/store/<string:name>/item", methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                "name": request_data['name'],
                "price": request_data['price']
            }
            store['item'].append(new_item)
            return jsonify(store)
    return jsonify({"message": "Store Not Found"})


app.run(port=5000)
