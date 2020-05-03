from werkzeug.security import safe_str_cmp
from models.user import UserModel

users = [
  # {
  #   'id': 1,
  #   'username': 'admin',
  #   'password': 'password'
  # }
  UserModel('admin', 'admin_password')
]

username_mapping = {
  # 'admin' : {
  #   'id': 1,
  #   'username': 'admin',
  #   'password': 'password'
  # }
  u.username : u for u in users
}

userid_mapping = {
  # 1: {
  #   'id': 1,
  #   'username': 'admin',
  #   'password': 'password'
  # }
  u.id : u for u in users
}

def authenticate(username, password):
  # user = username_mapping.get(username, None)
  user = UserModel.find_by_username(username)
  if user is not None and safe_str_cmp(user.password, password):
    return user

def identity(payload):
  print(payload)
  user_id = payload['identity']
  # return userid_mapping.get(user_id, None)
  return UserModel.find_by_id(user_id)
