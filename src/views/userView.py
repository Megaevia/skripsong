# /src/views/UserView

from flask import request, json, Response, Blueprint, g
from ..models.userModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

@user_api.route('/register', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = user_schema.load(req_data)
    if error:
        return custom_response(error, 400)

    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'Email already exist, please use another email'}
        message = {'error': 'Email sudah digunakan, silahkan gunakan email lainnya'}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()
    sch_data = user_schema.dump(user).data
    user_id = sch_data.get('id')
    token = Auth.generate_token(user_id)
    return custom_response({"user": user_id, "jwt_token": token}, 201)

@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)
    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to login'}, 400)
        #return custom_response({'error': 'you need email and password to sign in'}, 400)

    user = UserModel.get_user_by_email(data.get('email'))
    if not user:
        return custom_response({'error': 'invalid email'}, 400)
    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid password'}, 400)

    ser_data = user_schema.dump(user).data
    user_id = ser_data.get('id')
    token = Auth.generate_token(user_id)
    return custom_response({"user": user_id, "jwt_token": token}, 200)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  users = UserModel.get_one_user(g.user.get('id'))
  ser_users = user_schema.dump(users).data
  return custom_response(ser_users, 200)

@user_api.route('/me/update', methods=['PUT'])
@Auth.auth_required
def update():
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    # user_data = user_schema.dump(user).data
    return custom_response({"Message": "Data Updated!"}, 200)

@user_api.route('/me/delete', methods=['DELETE'])
@Auth.auth_required
def delete():
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({"Message": "Account Deleted!"}, 200)

def custom_response(res, status_code):
    return Response(
        mimetype = "application/json",
        response = json.dumps(res),
        status = status_code
    )
