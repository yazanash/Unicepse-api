import pyotp
from flask import Flask
from flask_mail import Mail , Message
from db import db

# from src.Training.routes.training_route import trainingBlueprint
# from src.Authentication.auth_routes import auth_Bp

app = Flask(__name__)
# app.register_blueprint(trainingBlueprint)
# app.register_blueprint(auth_Bp)
# app.app_context().push()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yazan.ash.doonaas@gmail.com'
app.config['MAIL_PASSWORD'] = 'kumjcthvitqbdyah'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


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
    app.run(debug=True, port=5151)
