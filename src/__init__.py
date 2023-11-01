import os

from flask import Flask
from src.Training.routes.training_route import trainingBlueprint
from src.Authentication.auth_routes import auth_Bp
import firebase_admin
from firebase_admin import credentials

from src.routes import general_Bp

app = Flask(__name__)
app.register_blueprint(trainingBlueprint)
app.register_blueprint(auth_Bp)
# app.register_blueprint(general_Bp)
app.config['SECRET_KEY'] = '8fbdb21ddb2142c1b356b7b57b6c9700'
os.environ['SECRET_KEY'] = app.config['SECRET_KEY']
cred = credentials.Certificate("key.json")
init = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://platinum-8b28f-default-rtdb.firebaseio.com"
})


@app.route("/", methods=["GET"])
def base():
    """this route for check connection"""
    return "PlatinumApi:v1.0.0"
