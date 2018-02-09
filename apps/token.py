import hashlib, random
from flask import Blueprint, jsonify, request
from helpers.user_helper import *
from helpers.token_helper import *
from models import Token, User, Code
from playhouse.shortcuts import model_to_dict, dict_to_model


app_token = Blueprint('app_token', __name__)


@app_token.route('/tokens', methods=['GET'])
def tokens():

    return jsonify({'error': False, 'tokens': list(Token.select().dicts()) }), 201


@app_token.route('/login', methods=['POST'])
def send():

    params = request.get_json()
    email= params.get('email')
    md5 = hashlib.md5()
    password = params.get('password')
    new_hash = hashlib.md5(password).hexdigest()

    try:
        user_found = User.get(User.email == email)
        
        if user_found.password == new_hash:
            code = Code.create(user_id=user_found.id, value=random.randint(1000, 9999), charge_id='empty')
            code.save()
            sender = "Aperture"
            text = "Here is your code {code} to authentify yourself.".format(code=code.value)
            sending_message = send_message(sender, text)
            return jsonify({'error': False, 'message': 'Your code has been sent'}), 201

        else :
            return jsonify({'error': True, 'message': 'Wrong email or password'}), 400

    except Exception as e:
        return jsonify({'error': True, 'message': e}), 400


@app_token.route('/auth', methods=['POST'])
def auth_user():

    params = request.get_json()
    user_code = params.get('code')
    user_id = params.get('user_id')

    try:
        user = User.get(User.id == user_id)
        code = Code.get(Code.user_id == user_id)

        if user_code == code.value:
            code.delete_instance()
            token_generated = generate_token()
            token_model = None

            try:
                token_model = Token.get(Token.user_id == user_id)
                data = model_to_dict(token_model)
                return jsonify({'error': False, 'message': 'User already has a token', 'token': data})

            except:
                token = create_token(token_generated, user_id)
                data = model_to_dict(token)
                return jsonify({'error': False, 'message': 'Token created', 'token': data})

        else :
            return jsonify({'error': True, 'message': 'Incorrect code'}), 400

    except Exception as identifier:
        return jsonify({'error': True, 'message': 'Error during authentification'}), 400