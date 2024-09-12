from datetime import datetime as date

from src.Authentication import profile_services
from src.common import points


class Profile(profile_services.ProfileService):

    def __init__(self, uid=None,
                 full_name=None,
                 phone=None,
                 birth_date=None,
                 gender_male=None,
                 level=None,
                 ):
        super().__init__()
        self.uid = uid
        self.full_name = full_name
        self.phone = phone
        self.birth_date = birth_date
        self.gender_male = gender_male
        self.level = level

    def serialize(self):
        """Serializes a User into a dictionary"""
        return {
            'uid': str(self.uid),
            'full_name': self.full_name,
            'phone': self.phone,
            'birth_date': self.birth_date,
            'gender_male': self.gender_male,
            'level': self.level / points.FULL_LEVEL_POINTS,
        }

    def deserialize(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.uid = data["uid"]
            self.full_name = data["full_name"]
            self.phone = data["phone"]
            self.birth_date = data["birth_date"]
            self.gender_male = data["gender_male"]
        except KeyError as error:
            raise profile_services.DataValidationError("Invalid Profile: missing " + error.args[0]) from error
        except TypeError as error:
            raise profile_services.DataValidationError(
                "Invalid Profile: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    def deserialize_from_database(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.uid = data["uid"]
            self.full_name = data["full_name"]
            self.phone = data["phone"]
            self.birth_date = data["birth_date"]
            self.gender_male = data["gender_male"]
            self.level = data["level"]
        except KeyError as error:
            raise profile_services.DataValidationError("Invalid Profile: missing " + error.args[0]) from error
        except TypeError as error:
            raise profile_services.DataValidationError(
                "Invalid Profile: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    def deserialize_by_token(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.full_name = data["full_name"]
            self.phone = data["phone"]
            self.birth_date = data["birth_date"]
            self.gender_male = data["gender_male"]
        except KeyError as error:
            raise profile_services.DataValidationError("Invalid Profile: missing " + error.args[0]) from error
        except TypeError as error:
            raise profile_services.DataValidationError(
                "Invalid Profile: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    @classmethod
    def create_model(cls):
        return Profile()

