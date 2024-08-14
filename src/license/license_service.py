from bson import ObjectId
from flask import make_response, jsonify
from marshmallow import ValidationError

from src.license.license_model import License
from src.license.license_validation import LicenseBaseSchema
from src.common import status

license_schema = LicenseBaseSchema()


class LicenseService:

    @staticmethod
    def create_license_use_case(json):
        """Creates licenses"""
        try:
            data = license_schema.load(json)
            if not License.check_if_exist(data['gym_id'], data['plan_id'], data['subscribe_date']):
                gym_license = License.create_model()
                gym_license.deserialize_secret(data)
                gym_license.create()
                return make_response(jsonify({"result": "Created successfully", "data": gym_license.serialize()}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_license_use_case(json, _id):
        """Update licenses"""
        try:
            data = license_schema.load(json)
            gym_license = License.find(_id)
            if gym_license is not None:
                gym_license.deserialize_secret(data)
                gym_license.update()
                return make_response(jsonify({"result": "Created successfully", "message": f"{gym_license.gym_id}"}),
                                     status.HTTP_200_OK)
            return make_response(jsonify({"result": "Not Exists Exception", "message": "this record is not exists"}),
                                 status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def read_licenses_use_case():
        """Reads All licenses"""
        licenses_list = License.all()
        if len(licenses_list) > 0:
            licenses_dict = [gym_license.serialize() for gym_license in licenses_list]
            return make_response(jsonify(licenses_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any licenses"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_license_use_case(_id):
        """Reads license"""
        gym_license = License.find(_id)
        if gym_license is not None:
            return make_response(jsonify(gym_license.serialize()),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_gym_licenses_use_case(gym_id):
        """Reads All licenses For gym"""
        print(f"service started to gym id {gym_id}")
        licenses_list = License.all_license(gym_id)
        if len(licenses_list) > 0:
            licenses_dict = [gym_license.serialize() for gym_license in licenses_list]
            return make_response(jsonify(licenses_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any licenses"}),
                             status.HTTP_200_OK)