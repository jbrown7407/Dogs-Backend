import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

#first argument is blueprints name
# second arg is its import_name
#third arg is url prefix
user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/register', methods=["POST"])
def register():
  payload = request.get_json()

  payload['email']= payload['email'].lower()
  try:
    models.Users.get(models.Users.email == payload['email'])
    return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists."})
  except models.DoesNotExist:
      payload['password'] = generate_password_hash(payload['password'])
      user = models.Users.create(**payload)

      login_user(user)

      user_dict = model_to_dict(user)
      print(user_dict)
      print(type(user_dict))

      del user_dict['pasword']

      return jsonify(data=user_dict, status={"code": 201. "message" "Success"})
