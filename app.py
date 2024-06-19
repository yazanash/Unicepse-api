import os
import pyotp

from flask import Flask


from src.Training.training_route import trainingBlueprint
from src.Authentication.auth_routes import auth_Bp
from src.metrics.metrics_routes import metrics_bp
from src.subscription.subscription_route import subscriptionBp
from src.payment.payment_route import payments_bp
from src.Player.player_route import playerBp
from mail import mail
app = Flask(__name__)

app.register_blueprint(trainingBlueprint)
app.register_blueprint(auth_Bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(subscriptionBp)
app.register_blueprint(payments_bp)
app.register_blueprint(playerBp)

app.app_context().push()

# app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
# app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
# app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
# app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yazan.ash.doonaas@gmail.com'
app.config['MAIL_PASSWORD'] = 'kumjcthvitqbdyah'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)


@app.route("/hello")
def hello():
    return "<h1>Hello<h1>"


@app.route("/", methods=["GET"])
def hello_app():
    return "Unicepse Api; version=1.0.0"


# @app.route("/send_mail")
# def index():
#     email = "yazan.ash.doonaas@gmail.com"
#     print(email)
#     msg = Message('Hello From Unicepse', sender='unicepse@gmail.com',
#                   recipients=[email])
#     secret = pyotp.random_base32()
#     totp = pyotp.TOTP(secret)
#     otp = totp.now()
#     print(otp)
#     # print(mail)
#     msg.body = f"Hello From unicepse this email is a test this is your otp {otp}"
#     mail.send(msg)
#     # print(mail)
#     return "Mail Sent please check"


if __name__ == "__main__":
    # app.run(debug=False, host="192.168.1.7", port=5000)
    app.run(debug=True, port=5000)
