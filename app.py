from flask import Flask
from src.Training.routes.training_route import trainingBlueprint
app = Flask(__name__)

app.register_blueprint(trainingBlueprint)


@app.route('/', methods=["GET"])
def hello_app():
    return "Platinum Api; version=1.0.0"


if __name__ == "__main__":
    app.run(debug=True)
