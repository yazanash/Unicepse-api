from flask import make_response, jsonify

from src.payment.payment_validator import validate_payment
from src.payment.payment_model import Payment
from src.common.errors import DataValidationError
from src.common import status


class PaymentService:

    @staticmethod
    def create_payment_use_case(json):
        """Creates payment for player subscription"""
        try:
            validate_payment(json)
            if not Payment.check_if_exist(json['gym_id'], json['pid'], json['sid'], json['id']):
                pay = Payment.create_model()
                pay.deserialize(json)
                pay.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{pay.id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except DataValidationError:
            return make_response(jsonify({"result": "Validation Error", "message": "required data is missing "}),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def read_payments_use_case(gym_id, pid, sid):
        """Reads All payments  for player subscription"""
        pays_list = Payment.all(gym_id, pid, sid)
        if len(pays_list) > 0:
            pays_dict = [pay.serialize() for pay in pays_list]
            print(pays_dict)
            return make_response(jsonify(pays_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_payment_use_case(gym_id, pid, sid, id):
        """Reads All payments  for player subscription"""
        pay = Payment.find(gym_id, pid, sid, id)
        if pay is not None:
            return make_response(jsonify(pay.serialize()),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update_payment_use_case(data):
        """update payment for player subscription"""
        try:
            validate_payment(data)
            pay = Payment.find(data['gym_id'], data['pid'], data['sid'], data['id'])
            if pay is None:
                return make_response(jsonify({"result": "Not found", "message": "this payment is not exist"}),
                                     status.HTTP_404_NOT_FOUND)
            pay=Payment.create_model()
            pay.deserialize(data)
            pay.update()
            return make_response(
                jsonify({"result": "Updated successfully", "message": "payment updated successfully "}),
                status.HTTP_200_OK)
        except DataValidationError:
            return make_response(jsonify({"result": "Validation Error",
                                          "message": "required data is missing "}),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_payment_use_case(gym_id, pid, sid, id):
        """delete payment for player subscription"""
        sub = Payment.find(gym_id, pid, sid, id)
        if not sub:
            return make_response(jsonify({"result": "Not found", "message": "this payment is not exist"}),
                                 status.HTTP_404_NOT_FOUND)
        sub.delete()
        return make_response(
            jsonify({"result": "Deleted successfully", "message": "payment deleted successfully "}),
            status.HTTP_200_OK)

