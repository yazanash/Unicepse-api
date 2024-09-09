import os

from PIL import Image
from flask import make_response, jsonify, send_from_directory
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

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
        if len(gyms) > 0:
            gyms_dict = []
            for gym in gyms:
                data = gym.serialize()
                handshake = HandShake.find_single(current_user.uid, gym.id)
                if handshake is not None:
                    data.update({"pid": handshake.pid, "created_at": handshake.created_at})
                print(data)
                gyms_dict.append(data)
            return make_response(jsonify(gyms_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def upload_logo_gym_use_case(data):
        """Reads All payments  for player subscription"""
        print("accessed 1")
        if 'file' not in data.files:
            return jsonify({'error': 'No file part'}), 400
        file = data.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        print("accessed 2")

        if file:
            filename = secure_filename(file.filename)
            print("accessed 3")
            file_path = os.path.join(os.environ['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Compress and convert to JPG
            output_filename = os.path.splitext(filename)[0] + '.jpg'
            output_path = os.path.join(os.environ['UPLOAD_FOLDER'], output_filename)

            with Image.open(file_path) as img:
                img = img.convert("RGB")  # Ensure image is in RGB mode
                img.save(output_path, "JPEG", quality=85)
            # Remove the original file
            os.remove(file_path)
            return jsonify({'message': 'File uploaded and compressed successfully', 'filename': output_filename}), 201

    @staticmethod
    def get_gym_logo_use_case(gym_id):
        """Reads All payments  for player subscription"""
        gym = Gym.find(gym_id)
        filename = gym.logo
        return send_from_directory(os.environ['UPLOAD_FOLDER'], filename)
