import os

from flask import Flask
from src.Training.routes.training_route import trainingBlueprint
from flask_mail import Mail, Message
from src.Authentication.routes.auth_routes import auth_Bp
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db

from src.routes import general_Bp
from src.Player.player_route import playerBp

app = Flask(__name__)
app.register_blueprint(trainingBlueprint)
app.register_blueprint(auth_Bp)
app.register_blueprint(playerBp)

# app.register_blueprint(general_Bp)
app.config['SECRET_KEY'] = '8fbdb21ddb2142c1b356b7b57b6c9700'
os.environ['SECRET_KEY'] = app.config['SECRET_KEY']
cred = credentials.Certificate("key.json")
init = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://platinum-8b28f-default-rtdb.firebaseio.com"
})
