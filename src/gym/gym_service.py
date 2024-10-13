import os
from io import BytesIO

from PIL import Image
from flask import make_response, jsonify, send_from_directory, send_file
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from firebase_helper import bucket
from src.Player.player_model import Player
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
                return make_response(jsonify({"result": "Created successfully", "gym_id": f"{gym.id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_gym_use_case(id, json):
        """update Gyms"""
        try:
            data = gym_schema.load(json)
            gym = Gym.find(id)
            if gym is not None:
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
        if len(handshakes) > 0:
            gyms_dict = []
            for handshake in handshakes:
                gym = Gym.find(handshake.gym_id)
                data = gym.serialize()
                print(handshake.gym_id + handshake.pid)
                player = Player.find(handshake.gym_id, handshake.pid)
                data.update({"pid": handshake.pid, "start": player.subs_date, "end": player.subs_end_date,
                             "created_at": handshake.created_at})
                gyms_dict.append(data)
            return make_response(jsonify(gyms_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def upload_logo_gym_use_case(data):
        """Reads All payments  for player subscription"""
        if 'file' in data.files:
            photo = data.files['file']
            blob = bucket.blob(photo.filename)
            blob.upload_from_file(photo)
            return f"Photo uploaded to Firebase Storage as {photo.filename}"
        return 'No photo uploaded'

    @staticmethod
    def upload(data):
        if 'file' in data.files:
            photo = data.files['file']
            gym_id = data.form['gym_id']
            blob = bucket.blob(gym_id)
            blob.upload_from_file(photo)
            return f"Photo uploaded to Firebase Storage as {photo.filename}"
        return 'No photo uploaded'

    @staticmethod
    def get_gym_logo_use_case(gym_id):
        """Reads All payments  for player subscription"""
        blob = bucket.blob(gym_id)
        if blob.exists():
            image_data = blob.download_as_bytes()
            return send_file(BytesIO(image_data), mimetype='image/jpeg')
        return 'Image not found', 404




