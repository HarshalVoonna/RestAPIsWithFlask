from flask import Flask, jsonify, request, render_template
import json

# print(__name__)
app = Flask(__name__)

stores = []

@app.route('/')
def home():
  return "Home Page says 'Hello World!'"
  # return render_template('index.html')

# POST /store {name:}
@app.route('/store', methods=['POST'])
def create_store():
  request_data = request.get_json()
  new_store = {
    'name': request_data['name'],
    'items': []
  }
  stores.append(new_store)
  return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
  for store in stores:
    if name == store['name']:
      return jsonify(store)
  return jsonify({"message": "Store Not Found"})

# GET /store
@app.route('/store')
def list_stores():
  return jsonify({"stores" : stores})

# POST /store/<string:name>/item {name:,price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def add_item_to_store(name):
  request_data = request.get_json()
  for store in stores:
    if store['name'] == name:
      new_item = {
        'name': request_data['name'],
        'price': request_data['price']
      }
      store['items'].append(new_item)
      return jsonify(store)

  return jsonify({"message": "Store Not Found"})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
  for store in stores:
    if store['name'] == name:
      return jsonify({'items': store['items']})
  return jsonify({"message": "Item Not Found"})

app.run(port=5000)
