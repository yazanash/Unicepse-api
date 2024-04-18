# from .subscription_model import Subscription
from src.common.errors import DataValidationError
from src.common.utils import logger
# from datetime import datetime


def validate_payment(json: dict):
    try:
        assert (type(json["id"]) is int)
        assert (type(json["pl_id"]) is int)
        assert (type(json["sub_id"]) is int)
        assert (type(json["gym_id"]) is int)
        # assert (type(json["description"]) is str)     Nullable
        assert (type(json["value"]) is int)
        assert (type(json["date"]) is str)
    except ValueError:
        logger.error("ValueError in payment data")
        raise DataValidationError("ValueError in payment")
    except AssertionError as e:
        logger.error("Assertion Error %s", e.args[0])
        raise DataValidationError("AssertionError in payment")
    except AttributeError as e:
        logger.error("Attribute Error %s", e.args[0])
        raise DataValidationError("Attribute Error!, datetime is probably (None)")
    except Exception as e:
        logger.error(f"payment Exception: {e.args[0]}")
        raise DataValidationError(f"Unknown Exception happened! {e.args[0]}")
