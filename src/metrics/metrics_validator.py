from src.common import errors
from src.common.utils import logger


def validate_metric(json: dict):

    try:
        assert (type(json["id"]) is int)
        assert (type(json["pl_id"]) is int)
        assert (type(json["met_id"]) is int)
        assert (type(json["gym_id"]) is int)
        assert (type(json["check_date"]) is str)
        assert (type(json['height'],) is float)
        assert (type(json['weight'],) is float)
        assert (type(json['l_arm'],) is float)
        assert (type(json['r_arm'],) is float)
        assert (type(json['l_humerus'],) is float)
        assert (type(json['r_humerus'],) is float)
        assert (type(json['l_thigh'],) is float)
        assert (type(json['r_thigh'],) is float)
        assert (type(json['l_leg']) is float)
        assert (type(json['r_leg']) is float)
        assert (type(json['neck']) is float)
        assert (type(json['shoulders']) is float)
        assert (type(json['waist']) is float)
        assert (type(json['chest']) is float)
        assert (type(json['hips']) is float)
    except ValueError:
        logger.error("ValueError in metric data")
        raise errors.DataValidationError("ValueError in metric")
    except AssertionError as e:
        logger.error("Assertion Error %s", e.args[0])
        raise errors.DataValidationError("AssertionError in metric")
    except AttributeError as e:
        logger.error("Attribute Error %s", e.args[0])
        raise errors.DataValidationError("Attribute Error!, datetime is probably (None)")
    except Exception as e:
        logger.error(f"payment Exception: {e.args[0]}")
        raise errors.DataValidationError(f"Unknown Exception happened! {e.args[0]}")
