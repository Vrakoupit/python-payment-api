import datetime, stripe, random
from flask import Blueprint, jsonify, request
from helpers.payment_helper import *
from helpers.user_helper import *
from models import Payment, User, Token, Code
from playhouse.shortcuts import model_to_dict, dict_to_model
from const import *


app_payment = Blueprint('app_payment', __name__)

stripe.api_key = STRIPE_API_KEY


@app_payment.route('/payments', methods=['POST'])
def create_payment():

    params = request.get_json()
    token_user = params.get('token')
    amount = params.get('amount')
    label = params.get('label')
    card_number = params.get('card_number')
    card_month = params.get('card_month')
    card_year = params.get('card_year')
    card_cvc = params.get('card_cvc')

    card = {
        "number": card_number,
        "exp_month": card_month,
        "exp_year": card_year,
        "cvc": card_cvc
    }
    token = stripe.Token.create(card=card)

    if check_token(token_user) is False:
        return jsonify({'error': True, 'message': 'Not connected or token expired'}), 400

    else:
        userToken = check_token(token_user)

        try:
            charge = stripe.Charge.create(card=token.id, currency="eur", amount=amount, capture=False)
            
            payment = Payment.create(amount=amount, label=label, user=userToken.user_id)
            payment.save()

            code = Code.create(user_id=userToken.user_id.id, value=random.randint(1000, 9999), charge_id=charge.id)
            code.save()

            sender = "Aperture"
            text = "Here is your code {code} to authentify your transaction.".format(code=code.value)
            sending_message = send_message(sender, text)

            return jsonify({'error': False, 'message': "A code to authentify your transaction has been sent to you."}), 201

        except Exception as e:
            return jsonify({'error': True, 'message': '{error}'.format(error=e) }), 400


@app_payment.route('/payments/verification', methods=['POST'])
def verify_payment():

    params = request.get_json()
    user_id = params.get('user_id')
    user_code = params.get('code')

    try:
        user = User.get(User.id == user_id)
        code = Code.get(Code.user_id == user_id)

        if user_code == code.value:
            charge = stripe.Charge.retrieve(code.charge_id)
            charge.capture()
            code.delete_instance()
            return jsonify({'error': False, 'transaction': charge.outcome})

        else :
            return jsonify({'error': True, 'message': 'Incorrect code'}), 400

    except Exception as identifier:
        return jsonify({'error': True, 'message': 'Error during process'}), 400


@app_payment.route('/payment/<id>', methods=['POST'])
def get_transaction(id):

    params = request.get_json()
    token = params.get('token')
    
    if check_token(token) is False:
        return jsonify({'error': True, 'message': 'Not connected or token expired'}), 400
    
    else:
        userToken = check_token(token)

    try:
        payment = Payment.get(Payment.id == id)
        
        if check_user(token, id) is False:
            return jsonify({'error': False, 'message': 'This user can not access this transaction'}), 400

        else:
            data = model_to_dict(payment)
            return jsonify({'data': data}), 201

    except Exception as error:
        return jsonify({'error': False, 'message': 'Not found {error}'.format(error=error) }), 400


@app_payment.route('/payments', methods=['GET'])
def get_all_transactions():

    params = request.get_json()
    token = params.get('token')

    if check_token(token) is False:
        return jsonify({'error': True, 'message': 'Not connected or token expired'}), 400

    else:
        userToken = check_token(token)
        return jsonify({'error': False, 'data': list(Transaction.select().where(Transaction.user == userToken.user).dicts())}), 201