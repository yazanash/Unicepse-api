"""
User Model

for validate user auth
"""
from src.common import models
from datetime import date


class User(models.PersistentBase):

    def __init__(self):
        super().__init__()
        self.uid = None
        self.username = None
        self.email = None
        self.password = None
        self.token = None
        self.date_joined = None

    def serialize(self):
        """Serializes a User into a dictionary"""
        return {
            "uid": self.uid,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'token': self.token

        }

    def deserialize(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.uid = data["uid"]
            self.username = data["username"]
            self.email = data["email"]
            self.password = data["password"]
            self.token = data["token"]
            self.date_joined = None
            date_joined = data.get("date_joined")
            if date_joined:
                self.date_joined = date.fromisoformat(date_joined)
            else:
                self.date_joined = date.today()
        except KeyError as error:
            raise models.DataValidationError("Invalid Account: missing " + error.args[0]) from error
        except TypeError as error:
            raise models.DataValidationError(
                "Invalid Account: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self
