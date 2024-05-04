import os

from flask import Flask
from flask_mail import Mail

from src.Training.routes.training_route import trainingBlueprint
from src.Authentication.auth_routes import auth_Bp
from src.metrics.metrics_routes import metrics_bp
from src.subscription.subscription_route import subscriptionBp
from src.payment.payment_route import payments_bp

import firebase_admin
from firebase_admin import credentials

from src.routes import general_Bp
from src.Player.player_route import playerBp

app = Flask(__name__)
app.register_blueprint(trainingBlueprint)
app.register_blueprint(auth_Bp)
app.register_blueprint(playerBp)
app.register_blueprint(metrics_bp)
app.register_blueprint(subscriptionBp)
app.register_blueprint(payments_bp)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yazan.ash.doonaas@gmail.com'
app.config['MAIL_PASSWORD'] = 'kumjcthvitqbdyah'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app.config['SECRET_KEY'] = '8fbdb21ddb2142c1b356b7b57b6c9700'
os.environ['SECRET_KEY'] = app.config['SECRET_KEY']
cred = credentials.Certificate("key.json")
init = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://platinum-8b28f-default-rtdb.firebaseio.com"
})


