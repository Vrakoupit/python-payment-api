import hashlib
from flask import Blueprint, jsonify, request
from helpers.user_helper import *
from models import User, Code
from playhouse.shortcuts import model_to_dict, dict_to_model


app_user = Blueprint('app_user', __name__)


@app_user.route('/users', methods=['POST'])
def create_user():
    
    params = request.get_json()
    email = params.get('email')
    mobile = params.get('mobile')
    password = params.get('password')
    password_hashed = hashlib.md5(password).hexdigest()

    if is_email_taken(email) is True:
        return jsonify({'error': True, 'message': 'Email already used'}), 400

    else:
        user = User.create(email=email, mobile=mobile, password=password_hashed)
        user.save()
        data = model_to_dict(user)
        return jsonify({'error': False, 'user': data}), 201
        

@app_user.route('/users', methods=['GET'])
def get_all_users():

    return jsonify({'error': False, 'users': list(User.select().dicts()) }), 201


@app_user.route('/user/<id>', methods=['GET'])
def get_user(id):

    try:
        user = User.get(User.id == id)
        data = model_to_dict(user)
        return jsonify({'error': False, 'user': data}), 201

    except Exception as identifier:
        return jsonify({'error': True, 'message': 'Not found {message}'.format(message=identifier.message)}), 400


@app_user.route('/user/<id>', methods=['PUT'])
def update_user(id):

    try:
        user = User.get(User.id == id)
        params = request.get_json()

        if params.get('email', None) is not None:
            user.name = params.get('email')

        if params.get('mobile', None) is not None:
            user.name = params.get('mobile')

        if params.get('password', None) is not None:
            user.password = hashlib.md5(params.get('password')).hexdigest()
        
        user.save()
        data = model_to_dict(user)
        return jsonify({'error': False, 'user': data}), 201
        
    except Exception as identifier:
        return jsonify({'error': True, 'message': 'Not found {message}'.format(message=identifier.message)}), 400


@app_user.route('/user/<id>', methods=['DELETE'])
def delete_user(id):

    try:
        user = User.get(User.id == id)
        user.delete_instance()
        return jsonify({'error': False, 'message': 'User deleted'}), 201

    except Exception as identifier:
        return jsonify({'error': True, 'message': 'Not found {message}'.format(message=identifier.message)}), 400
        

@app_user.route('/codes', methods=['GET'])
def test():
    return jsonify({'codes': list(Code.select().dicts()) }), 201