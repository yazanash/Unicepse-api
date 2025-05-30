import os
from dotenv import load_dotenv

from flask import Flask, send_from_directory
from pyfcm import FCMNotification

from src.attedence.attendance_routes import attendances_bp
from api.src.routine.routine_route import routineBlueprint
from src.Authentication.auth_routes import auth_Bp
from src.Authentication.profile_routes import profile_Bp
from api.src.gym.gym_routes import gyms_bp
from src.handshake.handshake_routes import handshakes_bp
from src.license.license_routes import licenses_bp
from src.metrics.metrics_routes import metrics_bp
from src.offer.offer_route import offers_bp
from src.plans.plan_route import plans_bp
from src.subscription.subscription_route import subscriptionBp
from src.payment.payment_route import payments_bp
from src.Player.player_route import playerBp
from mail import mail

app = Flask(__name__)


load_dotenv()

app.register_blueprint(routineBlueprint)
app.register_blueprint(auth_Bp)
app.register_blueprint(profile_Bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(subscriptionBp)
app.register_blueprint(payments_bp)
app.register_blueprint(playerBp)
app.register_blueprint(handshakes_bp)
app.register_blueprint(gyms_bp)
app.register_blueprint(licenses_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(offers_bp)
app.register_blueprint(attendances_bp)
app.app_context().push()

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route("/api/v1", methods=["GET"])
def hello_app():
    return "<h1>Unicepse Api; version=1.0.0<h1>"


push_service = FCMNotification(api_key=os.environ['SERVER_KEY'])


@app.route("/logo", methods=["GET"])
def app_logo():
    return send_from_directory(f'assets/logo', 'logo.png')


# @app.route('/api/v1/send_notify', methods=['POST'])
# def send_notification():
#     data = request.json
#     # registration_id = data.get('registration_id')
#     # message_title = data.get('title')
#     # message_body = data.get('body')
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=data.get('title'),
#             body=data.get('body'),
#         ),
#         token=data.get('registration_id'),
#     )
#     # result = push_service.notify_single_device(
#     #     registration_id=registration_id,
#     #     message_title=message_title,
#     #     message_body=message_body
#     # )
#     response = messaging.send(message)
#     print('Successfully sent message:', response)



if __name__ == "__main__":
    # app.run(debug=False, host="192.168.1.7", port=5000)
    app.run(debug=True, port=5000)
