# from flask import Flask
# from src.Training.routes.training_route import trainingBlueprint
# from flask_mail import Mail, Message
# from src.Authentication.routes.auth_routes import auth_Bp
# app = Flask(__name__)
# app.register_blueprint(trainingBlueprint)
# app.register_blueprint(auth_Bp)
# app.app_context().push()
#
# mail = Mail(app)
#
#
# @app.route('/', methods=["GET"])
# def hello_app():
#     return "Platinum Api; version=1.0.0"
#
#
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
