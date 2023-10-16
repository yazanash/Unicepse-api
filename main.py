from flask import Flask
app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_app():
    return "Platinum Api; version=1.0.0"


if __name__ == "__main__":
    app.run(debug=True)
