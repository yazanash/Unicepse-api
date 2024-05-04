import pyotp
from flask import Flask
from flask_mail import Mail, Message
import src
# from db import db

# from src.Training.routes.training_route import trainingBlueprint
# from src.Authentication.auth_routes import auth_Bp
# from src.metrics.metrics_routes import metrics_bp
# from src.subscription.subscription_route import subscriptionBp
# from src.payment.payment_route import payments_bp

app = Flask(__name__)

# app.register_blueprint(trainingBlueprint)
# app.register_blueprint(auth_Bp)
# app.register_blueprint(metrics_bp)
# app.register_blueprint(subscriptionBp)
# app.register_blueprint(payments_bp)

# app.app_context().push()

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'yazan.ash.doonaas@gmail.com'
# app.config['MAIL_PASSWORD'] = 'kumjcthvitqbdyah'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/hello")
def hello():
    return "<h1>Hello<h1>"


@app.route("/send_mail")
def index():
    email = "yazan.ash.doonaas@gmail.com"
    print(email)
    msg = Message('Hello From Unicepse', sender='unicepse@gmail.com',
                  recipients=[email])
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    print(otp)
    # print(mail)
    msg.body = f"Hello From unicepse this email is a test this is your otp {otp}"
    mail.send(msg)
    # print(mail)
    return "Mail Sent please check"


if __name__ == "__main__":
    # app.run(debug=False, host="192.168.1.7", port=5000)
    app.run(debug=True, port=5000)
