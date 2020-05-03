import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

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

    if UserModel.find_by_username(data['username']):
      return {'message': 'User is already present in the database'}, 400

    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    insert_query = 'INSERT INTO users VALUES(NULL, ?, ?)'
    result = cursor.execute(insert_query, (data['username'], data['password']))
    connection.commit()
    connection.close()
    """
    user = UserModel(**data)
    user.save_to_db()
    return {'message': 'User signed up successfully'}, 201
