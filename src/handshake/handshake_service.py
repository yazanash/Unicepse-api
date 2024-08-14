from flask import make_response, jsonify
from marshmallow import ValidationError

from src.handshake.handshake_model import HandShake
from src.handshake.hanshake_validation import HandShakeBaseSchema
from src.payment.payment_validator import validate_payment
from src.payment.payment_model import Payment
from src.common.errors import DataValidationError
from src.common import status

hand_shake_schema = HandShakeBaseSchema()


class HandShakeService:

    @staticmethod
    def create_hand_shack_use_case(json):
        """Creates payment for player subscription"""
        try:
            data = hand_shake_schema.load(json)
            if not HandShake.check_if_exist(data['gym_id'], data['pid'], data['uid']):
                handshake = HandShake.create_model()
                handshake.deserialize(data)
                handshake.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{handshake.uid}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
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

