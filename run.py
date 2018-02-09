from flask import Flask
from apps.user import app_user
from apps.token import app_token
from apps.payment import app_payment

app = Flask(__name__)
app.register_blueprint(app_user)
app.register_blueprint(app_token)
app.register_blueprint(app_payment)

if __name__ == "__main__":
    app.run(debug=True, port=3000)