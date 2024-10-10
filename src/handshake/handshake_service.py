from firebase_admin.messaging import UnregisteredError
from flask import make_response, jsonify
from marshmallow import ValidationError

import firebase_helper
from src.Authentication.profile_model import Profile
from src.Authentication.user_model import User
from src.attedence.attendance_model import Attendance
from src.gym.gym_model import Gym
from src.handshake.handshake_model import HandShake
from src.handshake.hanshake_validation import HandShakeBaseSchema
from src.metrics.metrics_model import Metric
from src.payment.payment_validator import validate_payment
from src.payment.payment_model import Payment
from src.common.errors import DataValidationError
from src.common import status, points, notification_messages
from src.routine.routine_model import Routine
from src.subscription.subscription_model import Subscription

hand_shake_schema = HandShakeBaseSchema()


class HandShakeService:

    @staticmethod
    def create_hand_shack_use_case(json):
        """Creates payment for player subscription"""
        try:
            data = hand_shake_schema.load(json)
            user = User.find(data['uid'])
            if user is not None:
                if not HandShake.check_if_exist(data['gym_id'], data['uid']):
                    handshake = HandShake.create_model()
                    handshake.deserialize(data)
                    handshake.create()
                    handshake.set_level()
                    gym = Gym.find(handshake.gym_id)
                    title = f"اهلا بك في عائلة {gym.gym_name} ."
                    handshake.send_notification(title, notification_messages.HANDSHAKE_MESSAGE)
                    return make_response(jsonify({"result": "Created successfully", "message": f"{handshake.uid}"}),
                                         status.HTTP_201_CREATED)
                return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                     status.HTTP_409_CONFLICT)
            return make_response(jsonify({"result": "Not found Exception", "message": "this USER is NOT exists"}),
                                 status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def read_hand_shakes_use_case(uid):
        """Reads All payments  for player subscription"""
        handshakes_list = HandShake.all(uid)
        if len(handshakes_list) > 0:
            handshake_dict = [handshake.serialize() for handshake in handshakes_list]
            return make_response(jsonify(handshake_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_hand_shake_use_case(uid):
        """Reads All payments  for player subscription"""
        handshake = HandShake.all(uid)
        if handshake is not None:
            return make_response(jsonify(handshake.serialize()),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def send_gym_players_notifications_use_case(gym_id, json):
        """Creates payment for player subscription"""
        handshakes = HandShake.all_by_gym(gym_id)
        if handshakes is not None:
            for handshake in handshakes:
                handshake.send_notification(json['title'], json['body'])
            return make_response(jsonify({"message": "notification sent successfully"}), status.HTTP_200_OK)
        return make_response(jsonify({"message": "notification sent successfully"}), status.HTTP_404_NOT_FOUND)

    @staticmethod
    def send_all_players_notifications_use_case(json):
        """Creates payment for player subscription"""
        users = User.all()
        if users is not None:
            for user in users:
                try:
                    firebase_helper.send_notification(user.notify_token,'title', 'body')
                except UnregisteredError as ex:
                    continue
                except ValueError as ex:
                    continue
            return make_response(jsonify({"message": "notification sent successfully"}), status.HTTP_200_OK)
        return make_response(jsonify({"message": "notification sent successfully"}), status.HTTP_404_NOT_FOUND)
