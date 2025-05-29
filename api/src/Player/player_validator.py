from datetime import datetime
from src.common.utils import logger
from src.common.errors import DataValidationError


def validate_player(json):
    try:

        # assert (type(json["pid"]) is int)                 # NULLABLE
        assert (type(json["name"]) is str)
        # assert (type(json['width']) is float)             # NULLABLE
        # assert (type(json['height']) is float)            # NULLABLE
        assert (type(json['date_of_birth']) is int)
        assert (type(json['gender']) is str)
        # assert (type(json['balance']) is int)             # NULLABLE
    except ValueError:
        logger.error("ValueError in player data")
        raise DataValidationError("ValueError in player")
    except AssertionError:
        logger.error("AssertionError in player data")
        raise DataValidationError("AssertionError in player")
    except AttributeError as e:
        logger.error("Attribute Error %s", e.args[0])
        raise DataValidationError("Attribute Error!   datetime is probably (None)")
    except Exception:
        logger.error("Unknown Exception happened IN PLAYER VALIDATOR")
        raise DataValidationError("Unknown Exception happened!")
