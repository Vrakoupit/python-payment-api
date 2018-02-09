from models import User
from const import *
import nexmo


# Check if the email is available
def is_email_taken(email_sent):
    try:
        user = User.get(User.email == email_sent)
        return True
    except:
        return False


# Sends a message to a mobile
def send_message(sender, text):
    client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
    response = client.send_message({
        'from': sender,
        'to': NEXMO_TEST_PHONE,
        'text': text
    })
    response = response['messages'][0]

    if response['status'] == '0':
        print 'Sent message', response['message-id']
        print 'Remaining balance is', response['remaining-balance']
    else:
        print 'Error:', response['error-text']