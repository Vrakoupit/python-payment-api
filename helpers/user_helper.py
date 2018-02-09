from models import User
import nexmo

api_key = 'b703a97b'
api_secret = 'efd64976044f3ed9'

def is_email_taken(email_sent):
    try:
        user = User.get(User.email == email_sent)
        return True
    except:
        return False


def send_message(sender, text):
    client = nexmo.Client(key=api_key, secret=api_secret)
    response = client.send_message({
        'from': sender,
        'to': '+33668872918',
        'text': text
    })
    response = response['messages'][0]

    if response['status'] == '0':
        print 'Sent message', response['message-id']
        print 'Remaining balance is', response['remaining-balance']
    else:
        print 'Error:', response['error-text']