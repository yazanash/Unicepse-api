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
            if not Payment.check_if_exist(json['gym_id'], json['pl_id'], json['sub_id'], json['id']):
                pay = Payment.deserialize(json)
                pay.create()
                return status.HTTP_201_CREATED
            return status.HTTP_409_CONFLICT
        except DataValidationError:
            return status.HTTP_400_BAD_REQUEST

    @staticmethod
    def read_payment_use_case(data):
        """Reads All payments  for player subscription"""
        pays_list = Payment.all_json(data["gym_id"], data["pl_id"], data["sub_id"])
        if len(pays_list) > 0:
            return {pays_list.__str__()}, status.HTTP_200_OK
        return status.HTTP_204_NO_CONTENT

    @staticmethod
    def update_payment_use_case(data):
        """update payment for player subscription"""
        validate_payment(data)
        pay = Payment.find(data['gym_id'], data['pl_id'], data['sub_id'], data['id'])
        if not pay:
            return status.HTTP_404_NOT_FOUND
        pay.deserialize(data)
        pay.update()
        return "payment updated successfully ", status.HTTP_200_OK

    @staticmethod
    def delete_payment_use_case(data):
        """delete payment for player subscription"""
        sub = Payment.find(data['gym_id'], data['pl_id'], data['sub_id'], data['id'])
        if not sub:
            return status.HTTP_404_NOT_FOUND
        sub.delete()
        return "payment deleted successfully ", status.HTTP_200_OK

