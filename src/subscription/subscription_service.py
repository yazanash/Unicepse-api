from .subscription_validator import validate_subscription
from .subscription_model import Subscription
from src.common.errors import DataValidationError
from src.common import status


class SubscriptionService:

    @staticmethod
    def create_subscription_use_case(json):
        """Creates Subscription-subscription for player"""
        try:
            validate_subscription(json)
            if not Subscription.check_if_exist(json['pl_id'], json['id']):
                subs = Subscription.deserialize(json)
                subs.create()
                return status.HTTP_201_CREATED
            return status.HTTP_409_CONFLICT
        except DataValidationError:
            return status.HTTP_400_BAD_REQUEST

    @staticmethod
    def read_subscription_use_case(pl_id):
        """Reads All Subscription-subscription for player"""
        subs_list = Subscription.all_json(pl_id)
        if len(subs_list) > 0:
            return {subs_list.__str__()}, status.HTTP_200_OK
        return status.HTTP_204_NO_CONTENT

    @staticmethod
    def update_subscription_use_case(data):
        """update subscription for player"""
        validate_subscription(data)
        sub = Subscription.find(data['pl_id'], data['id'])
        if not sub:
            return status.HTTP_404_NOT_FOUND
        sub.deserialize(data)
        sub.update()
        return "subscription updated successfully ", status.HTTP_200_OK

    @staticmethod
    def delete_subscription_use_case(data):
        """delete subscription for player"""
        sub = Subscription.find(data['pl_id'], data['id'])
        if not sub:
            return status.HTTP_404_NOT_FOUND
        sub.delete()
        return "subscription deleted successfully ", status.HTTP_200_OK

