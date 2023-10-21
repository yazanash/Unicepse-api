import firebase_admin
from flask import Flask
from src.Training.routes.training_route import trainingBlueprint
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import os
app = Flask(__name__)

app.register_blueprint(trainingBlueprint)

print("get env var %s", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://platinum-8b28f-default-rtdb.firebaseio.com"
})
ref = db.reference("users")
print(ref.get())
# ref = db.reference('users')
# print(ref.get())
#
# user = auth.create_user(
#     email='user@example.com',
#     email_verified=False,
#     phone_number='+15555550100',
#     password='secretPassword',
#     display_name='John Doe',
#     disabled=False)
# print('Successfully created new user: {0}'.format(user.email))
#
# email = "user@example.com"
# user = auth.get_user_by_email(email)
# print('Successfully fetched user data: {0}'.format(user.password))


@app.route('/', methods=["GET"])
def hello_app():
    return "Platinum Api; version=1.0.0"


@app.route('/test-firebase', methods=["GET"])
def fire_app():
    return "none"


if __name__ == "__main__":
    app.run(debug=True, port=3000)
