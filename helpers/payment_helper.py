from models import User, Token, Payment
import datetime


# Check if the token sent exists
def check_token(tokenString):
    try:
        token = Token.get(Token.value == tokenString)

        if (token.created_at + datetime.timedelta(seconds=3600)) > datetime.datetime.now():
            return token
        
        else:
            token.delete_instance()
            return False
    
    except Exception as error:
        return False


# Check if the token and payment id sent are associated to a transaction
def check_user(token, payment):
    try:
        test_token = Token.get(Token.value == token)
        test_payment = Payment.get(Payment.id == payment)
    
        if test_token.user_id.id == test_payment.user.id:
            return True
        else:
            return False
    
    except Exception as error:
        return False