from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price',
                      type=float,
                      required=True,
                      help='This field cannot be left blank!'
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
    item = self.find_by_name(name)
    if item:
      return item, 200
    return {'message': 'Item not found'}, 404

  @classmethod
  def find_by_name(self, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    get_query = 'SELECT * FROM items where name=?'
    result = cursor.execute(get_query, (name,))
    row = result.fetchone()
    connection.close()
    if row:
      return {'item': {'name': row[0], 'price': row[1]}}

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
    item = self.find_by_name(name)
    if item:
      return {'message': 'Item with name {} already exists'.format(name)}, 400

    data = Item.parser.parse_args()
    item = {'name': name, 'price': data['price']}
    try:
      self.insert(item)
    except:
      return {'message': 'An error occurred inserting the item'}, 500
    return item, 201

  @classmethod
  def insert(self, item):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    insert_query = 'INSERT INTO items VALUES(?, ?)'
    cursor.execute(insert_query, (item['name'], item['price']))
    connection.commit()
    connection.close()

  @jwt_required()
  def delete(self, name):
    """
    global items
    items = list(filter(lambda x: x['name'] != name, items))
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    delete_query = 'DELETE FROM items WHERE name = ?'
    cursor.execute(delete_query, (name,))
    connection.commit()
    connection.close()
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
    item = self.find_by_name(name)
    updated_item = {'name': name, 'price': data['price']}
    if item is None:
      try:
        self.insert(updated_item)
      except:
        return {'message': 'An error occurred inserting the item'}, 500
    else:
      try:
        self.update(updated_item)
      except:
        return {'message': 'An error occurred updating the item'}, 500

    return updated_item, 200

  @classmethod
  def update(cls, item):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    update_query = 'UPDATE items SET price=? where name=?'
    cursor.execute(update_query, (item['price'], item['name']))
    connection.commit()
    connection.close()

class ItemList(Resource):
  @jwt_required()
  def get(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'SELECT * from items'
    result = cursor.execute(query)
    items = []
    for row in result:
      items.append({'name': row[0], 'price': row[1]})
    connection.close()

    return {'items': items}, 200