from flask import make_response, jsonify

from .subscription_validator import validate_subscription
from .subscription_model import Subscription
from src.common.errors import *
from src.common import status
from ..payment.payment_model import Payment


class SubscriptionService:

    @staticmethod
    def create_subscription_use_case(json):
        """Creates Subscription-subscription for player"""
        try:
            # validate_subscription(json)
            if not Subscription.check_if_exist(json['gym_id'], json['pid'], json['id']):
                subs = Subscription.create_model()
                subs.deserialize(json)
                subs.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{subs.id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except DataValidationError:
            return make_response(jsonify({"result": "Validation Error", "message": "required data is missing "}),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def read_subscription_use_case(gym_id, pid):
        """Reads All Subscription-subscription for player"""
        subs_list = Subscription.all(gym_id, pid)
        if len(subs_list) > 0:
            subs_dict = {}
            for subs in subs_list:
                sub_dict = {}
                sub_dict.update(subs.serialize())
                payment_list = Payment.all(gym_id, pid, subs.id)
                print(payment_list)
                pay_dict = [payment.serialize() for payment in payment_list]
                sub_dict.update({"payments": pay_dict})
                subs_dict.update(sub_dict)
            return make_response(jsonify(subs_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any transactions"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_single_subscription_use_case(gym_id, pid, id):
        """Reads All Subscription-subscription for player"""
        subs = Subscription.find(gym_id, pid,id)
        if subs is not None:
            return make_response(jsonify(subs.serialize()),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any transactions"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update_subscription_use_case(data):
        """update subscription for player"""
        validate_subscription(data)
        sub = Subscription.find(data['gym_id'], data['pid'], data['id'])
        if not sub:
            return make_response(jsonify({"result": "Not found", "message": "this transaction is not exist"}),
                                 status.HTTP_404_NOT_FOUND)
        sub = Subscription.create_model()
        sub.deserialize(data)
        sub.update()
        return make_response(jsonify({"result": "Updated successfully", "message": "subscription updated successfully "}),
                             status.HTTP_200_OK)


