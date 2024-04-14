from flask import Flask
from flask_mail import Mail
from db import db

from src.Training.routes.training_route import trainingBlueprint
from src.Authentication.auth_routes import auth_Bp

app = Flask(__name__)
app.register_blueprint(trainingBlueprint)
app.register_blueprint(auth_Bp)
app.app_context().push()

mail = Mail(app)


@app.route('/', methods=["GET"])
def hello_app():
    if db.todos.find():
        db.todos.insert_one({"Todos": {"Todos": "somevalue"}})
    res = db.todos.find()[0]

    return str(res)


if __name__ == "__main__":
    app.run(debug=True, port=5151)
