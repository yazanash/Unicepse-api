from flask import make_response, jsonify
from marshmallow import ValidationError

from src.gym.gym_model import Gym
from src.gym.gym_validation import GymBaseSchema
from src.handshake.handshake_model import HandShake
from src.handshake.hanshake_validation import HandShakeBaseSchema
from src.payment.payment_validator import validate_payment
from src.payment.payment_model import Payment
from src.common.errors import DataValidationError
from src.common import status

gym_schema = GymBaseSchema()


class GymService:

    @staticmethod
    def create_gym_use_case(json):
        """Creates Gyms"""
        try:
            data = gym_schema.load(json)
            if not Gym.check_if_exist(data['gym_name']):
                gym = Gym.create_model()
                gym.deserialize(data)
                gym.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{gym.id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_gym_use_case(json):
        """update Gyms"""
        try:
            data = gym_schema.load(json)
            if Gym.find(data['id']) is not None:
                gym = Gym.create_model()
                gym.deserialize(data)
                gym.update()
                return make_response(jsonify({"result": "Updated successfully", "message": f"{gym.id}"}),
                                     status.HTTP_200_OK)
            return make_response(jsonify({"result": "Not found Exception", "message": "this record is not exists"}),
                                 status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def read_gym_use_case(id):
        """Reads All payments  for player subscription"""
        gym = Gym.find(id)
        if gym is not None:
            return make_response(jsonify(gym.serialize()),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any gyms"}),
                             status.HTTP_404_NOT_FOUND)

    @staticmethod
    def read_gyms_use_case():
        """Reads All payments  for player subscription"""
        gyms = Gym.all()
        if len(gyms) > 0:
            gyms_dict = [gym.serialize() for gym in gyms]
            return make_response(jsonify(gyms_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_user_gyms_use_case(current_user):
        """Reads All payments  for player subscription"""
        gyms = Gym.all()
        handshakes = HandShake.all(current_user.uid)
        if len(gyms) > 0:
            gyms_dict = {}
            for gym in gyms:
                data = gym.serialize()
                handshake = HandShake.find_single(current_user.uid, gym.id)
                if handshake is not None:
                    data.update({"pid": handshake.pid, "created_at": handshake.created_at})
                gyms_dict.update(data)
            return make_response(jsonify(gyms_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

