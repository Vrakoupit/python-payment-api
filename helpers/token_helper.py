import os, binascii
from models import Token


# Generate a token
def generate_token():
    token_gen = binascii.b2a_hex(os.urandom(16))
    return token_gen


# Create a token to a specific user
def create_token(token, user_id):
    token = Token.create(value=token, user_id=user_id)
    token.save()
    return token