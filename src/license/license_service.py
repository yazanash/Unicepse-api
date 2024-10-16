from datetime import datetime

from flask import make_response, jsonify
from marshmallow import ValidationError

from src.license.license_model import License
from src.license.license_validation import LicenseBaseSchema
from src.common import status
from src.plans.plan_model import Plan

license_schema = LicenseBaseSchema()


class LicenseService:

    @staticmethod
    def create_license_use_case(json):
        """Creates licenses"""
        try:
            data = license_schema.load(json)
            if not License.check_if_exist(data['gym_id'], data['plan_id'], data['subscribe_date']):
                gym_license = License.create_model()
                plan = Plan.find(data['plan_id'])
                gym_license.deserialize_secret(data)
                gym_license.price = plan.price
                gym_license.period = plan.period
                gym_license.create()
                return make_response(jsonify(gym_license.serialize_without_token()),
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
                plan = Plan.find(data['plan_id'])
                gym_license.deserialize_secret(data)
                gym_license.price = plan.price
                gym_license.period = plan.period
                gym_license.update()
                return make_response(jsonify(gym_license.serialize_without_token()),
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
            licenses_dict = []
            for gym_license in licenses_list:
                plan = Plan.find(gym_license.plan_id)
                if plan is not None:
                    obj = {
                        '_id': str(gym_license._id),
                        'gym_id': gym_license.gym_id,
                        'plan_name': plan.plan_name,
                        'plan_id': plan.id,
                        'subscribe_date': gym_license.subscribe_date,
                        'subscribe_end_date': gym_license.subscribe_end_date,
                        'price': gym_license.price,
                        'period': gym_license.period,
                    }
                    licenses_dict.append(obj)
            return make_response(jsonify(licenses_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any licenses"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_license_use_case(_id):
        """Reads license"""
        gym_license = License.find(_id)
        if gym_license is not None:
            plan = Plan.find(gym_license.plan_id)
            if plan is not None:
                obj = {
                    '_id': str(gym_license._id),
                    'gym_id': gym_license.gym_id,
                    'plan_name': plan.plan_name,
                    'plan_id': str(plan.id),
                    'subscribe_date': gym_license.subscribe_date,
                    'subscribe_end_date': gym_license.subscribe_end_date,
                    'price': gym_license.price,
                    'period': gym_license.period,
                }
                return make_response(jsonify(obj), status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_license_info_use_case(_id):
        """Reads license"""
        gym_license = License.find(_id)
        if gym_license is not None:
            plan = Plan.find(gym_license.plan_id)
            if plan is not None:
                obj = {
                    '_id': str(gym_license._id),
                    'gym_id': gym_license.gym_id,
                    'plan': plan.plan_name,
                    'plan_id': str(plan.id),
                    'subscribe_date': gym_license.subscribe_date,
                    'subscribe_end_date': gym_license.subscribe_end_date,
                    'price': gym_license.price,
                    'period': gym_license.period,
                    'token': gym_license.token,
                }
                return make_response(jsonify(obj), status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)


    @staticmethod
    def read_license_use_case_with_product_key(_id):
        """Reads license"""
        gym_license = License.find(_id)
        if gym_license is not None:
            plan = Plan.find(gym_license.plan_id)
            if plan is not None:
                obj = {
                    '_id': str(gym_license._id),
                    'gym_id': gym_license.gym_id,
                    'plan_name': plan.plan_name,
                    'plan_id': plan.id,
                    'subscribe_date': gym_license.subscribe_date,
                    'subscribe_end_date': gym_license.subscribe_end_date,
                    'price': gym_license.price,
                    'product_key': gym_license.product_key,
                    'period': gym_license.period,
                }
                return make_response(jsonify(obj), status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def verify_license_use_case(current_license):
        """Reads license"""
        gym_license = License.find(current_license._id)
        if gym_license is not None:
            if gym_license.subscribe_end_date > datetime.now():
                return make_response(jsonify({"result": "Verified ", "message": "verified successfully"}),
                                     status.HTTP_202_ACCEPTED)
            return make_response(jsonify({"result": "Expired", "message": "license is expired"}),
                                 status.HTTP_406_NOT_ACCEPTABLE)
        return make_response(jsonify({"result": "No License", "message": "license is not exist"}),
                             status.HTTP_404_NOT_FOUND)

    @staticmethod
    def read_license_by_product_key_use_case(product_key):
        """Reads license"""
        gym_license = License.find_by_product_key(product_key)
        if gym_license is not None:
            plan = Plan.find(gym_license.plan_id)
            if plan is not None:
                obj = {
                    '_id': str(gym_license._id),
                    'gym_id': gym_license.gym_id,
                    'plan': plan.plan_name,
                    'subscribe_date': gym_license.subscribe_date,
                    'subscribe_end_date': gym_license.subscribe_end_date,
                    'token': gym_license.token,
                    'price': gym_license.price,
                    'period': gym_license.period,
                }
                gym_license.disable_product_key()
                return make_response(jsonify(obj), status.HTTP_200_OK)
            return make_response(jsonify({"result": "No content", "message": "cannot found any plans"}),
                                 status.HTTP_204_NO_CONTENT)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_gym_licenses_use_case(gym_id):
        """Reads All licenses For gym"""
        licenses_list = License.all_license(gym_id)
        if len(licenses_list) > 0:
            licenses_dict = []
            for gym_license in licenses_list:
                plan = Plan.find(gym_license.plan_id)
                if plan is not None:
                    obj = {
                        '_id': str(gym_license._id),
                        'gym_id': gym_license.gym_id,
                        'plan_name': plan.plan_name,
                        'plan_id': str(plan.id),
                        'subscribe_date': gym_license.subscribe_date,
                        'subscribe_end_date': gym_license.subscribe_end_date,
                        'price': gym_license.price,
                        'period': gym_license.period,
                    }
                    licenses_dict.append(obj)
            return make_response(jsonify(licenses_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any licenses"}),
                             status.HTTP_204_NO_CONTENT)
