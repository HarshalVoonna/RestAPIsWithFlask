from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price',
                      type=float,
                      required=True,
                      help='This field cannot be left blank!'
                      )
  parser.add_argument('store_id',
                      type=int,
                      required=True,
                      help='Store ID cannot be left blank!'
                      )

  @jwt_required()
  def get(self, name):
    """
    for item in items:
      if item['name'] == name:
        return item
    item = next(filter(lambda x: x['name'] == name, items), None)
    return {'item': item}, 200 if item else 404
    """
    item = ItemModel.find_by_name(name)
    if item:
      return item.json(), 200
    return {'message': 'Item not found'}, 404

  @jwt_required()
  def post(self, name):
    """
    if next(filter(lambda x: x['name'] == name, items), None) is not None:
      return {'message': 'Item with name {} already exists'.format(name)}, 400

    # data = request.get_json(silent=True)
    data = Item.parser.parse_args()

    item = {'name': name, 'price': data['price']}
    items.append(item)
    return item, 201
    """
    item = ItemModel.find_by_name(name)
    if item:
      return {'message': 'Item with name {} already exists'.format(name)}, 400

    data = Item.parser.parse_args()
    item = ItemModel(name, **data)
    try:
      item.save_to_db()
    except:
      return {'message': 'An error occurred inserting the item'}, 500
    return item.json(), 201

  @jwt_required()
  def delete(self, name):
    """
    global items
    items = list(filter(lambda x: x['name'] != name, items))
    """
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    delete_query = 'DELETE FROM items WHERE name = ?'
    cursor.execute(delete_query, (name,))
    connection.commit()
    connection.close()
    return {'message': 'Item has been deleted'}
    """
    item = ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
    return {'message': 'Item has been deleted'}

  @jwt_required()
  def put(self, name):
    # data = request.get_json(silent=True)
    data = Item.parser.parse_args()

    """
    item = next(filter(lambda x: x['name'] == name, items), None)
    if item is None:
      item = {'name': name, 'price': data['price']}
      items.append(item)
    else:
      item.update(data)
    return item
    """
    item = ItemModel.find_by_name(name)
    if item is None:
      item = ItemModel(name, **data)
    else:
      item.price = data['price']
      item.store_id = data['store_id']
    item.save_to_db()
    return item.json(), 200


class ItemList(Resource):
  @jwt_required()
  def get(self):
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'SELECT * from items'
    result = cursor.execute(query)
    items = []
    for row in result:
      items.append({'name': row[0], 'price': row[1]})
    connection.close()
    return {'items': items}, 200
    """
    return {'items': [item.json() for item in ItemModel.query.all()]}