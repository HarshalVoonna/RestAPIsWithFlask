import sqlite3
from flask_restful import Resource, reqparse

class User():
  def __init__(self, _id, username, password):
    self.id = _id
    self.username = username
    self.password = password

  @classmethod
  def find_by_username(cls, username):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM users WHERE username=?'
    result = cursor.execute(query, (username,))
    row = result.fetchone()
    if row:
      user = cls(*row)
    else:
      user = None
    connection.close()
    return user

  @classmethod
  def find_by_id(cls, _id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM users WHERE id=?'
    result = cursor.execute(query, (_id,))
    row = result.fetchone()
    if row:
      user = cls(*row)
    else:
      user = None
    connection.close()
    return user

class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username',
                      type=str,
                      required=True,
                      help="This field is required")
  parser.add_argument('password',
                      type=str,
                      required=True,
                      help="This field is required")

  def post(self):
    data =  UserRegister.parser.parse_args()

    if User.find_by_username(data['username']):
      return {'message': 'User is already present in the database'}, 400

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    insert_query = 'INSERT INTO users VALUES(NULL, ?, ?)'
    result = cursor.execute(insert_query, (data['username'], data['password']))
    connection.commit()
    connection.close()
    return {'message': 'User signed up successfully'}, 201
