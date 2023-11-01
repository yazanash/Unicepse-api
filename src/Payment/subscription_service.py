from .subscription_validator import validate_subscription
from .subscription_model import Subscription
from src.common.errors import DataValidationError
from src.common import status


class SubscriptionService:

    def create_subscription_usecase(self, json):
        """Creates Subscription-Payment for player"""
        try:
            validate_subscription(json)
            if not Subscription.check_if_exist(json['pl_id'], json['id']):
                subs = Subscription.deserialize(json)
                subs.create()
                return status.HTTP_201_CREATED
            return status.HTTP_409_CONFLICT
        except DataValidationError:
            return status.HTTP_400_BAD_REQUEST

    def read_subscription_usecase(self, pl_id):
        """Reads All Subscription-Payment for player"""
        subs_list = Subscription.all_json(pl_id)
        print("read all_json: ", subs_list)
        if len(subs_list) > 0:
            return {subs_list.__str__()}, status.HTTP_200_OK
        return status.HTTP_204_NO_CONTENT
