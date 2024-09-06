# from .subscription_model import Subscription
from src.common.errors import DataValidationError
from src.common.utils import logger
# from datetime import datetime


def validate_subscription(json: dict):
    try:
        assert (type(json["id"]) is str)
        assert (type(json["pid"]) is str)
        assert (type(json['sport_name']) is str)
        assert (type(json['trainer_name']) is str)
        # assert (type(json['price']) is int)
        # assert (type(json['start_date']) is str)
        # assert (type(json['end_date']) is str)
        # assert (type(json['discount_value']) is int)      #  NULLABLE
        # assert (type(json['discount_des']) is str)        #  NULLABLE
        # assert (type(json['is_payed']) is bool)           #  NULLABLE
        # assert (type(json['list_of_payments']) is list)   #  NULLABLE

    except ValueError:
        logger.error("ValueError in Subscription data")
        raise DataValidationError("ValueError in Subscription")
    except AssertionError:
        raise DataValidationError("AssertionError in Subscription")
    except AttributeError as e:
        logger.error("Attribute Error %s", e.args[0])
        raise DataValidationError("Attribute Error!, datetime is probably (None)")
    except Exception as e:
        logger.error(f"Subscription Exception: {e.args[0]}")
        raise DataValidationError(f"Unknown Exception happened! {e.args[0]}")
