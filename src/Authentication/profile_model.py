from datetime import datetime as date

from src.Authentication import profile_services


class Profile(profile_services.ProfileService):

    def __init__(self, uid=None,
                 full_name=None,
                 phone=None,
                 birth_date=None,
                 gender_male=None,
                 weight=None,
                 height=None
                 ):
        super().__init__()
        self.uid = uid
        self.full_name = full_name
        self.phone = phone
        self.birth_date = birth_date
        self.gender_male = gender_male
        self.weight = weight
        self.height = height

    def serialize(self):
        """Serializes a User into a dictionary"""
        return {
            'uid': str(self.uid),
            'full_name': self.full_name,
            'phone': self.phone,
            'birth_date': self.birth_date,
            'gender_male': self.gender_male,
            'weight': self.weight,
            'height': self.height
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
            self.weight = data["weight"]
            self.height = data["height"]
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
            self.weight = data["weight"]
            self.height = data["height"]
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

