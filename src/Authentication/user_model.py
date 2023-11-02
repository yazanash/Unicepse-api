"""
User Model

for validate user auth
"""

from datetime import datetime as date

from src.Authentication import models


class User(models.AuthService):

    def __init__(self, uid=None,
                 username=None,
                 email=None,
                 password=None,
                 token=None,
                 date_joined=None):
        super().__init__()
        self.uid = uid
        self.username = username
        self.email = email
        self.password = password
        self.token = token
        self.date_joined = date_joined

    dt_name = "user"

    def serialize(self):
        """Serializes a User into a dictionary"""
        return {
            'uid': str(self.uid),
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'date_joined': self.date_joined
        }

    def deserialize(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        # print(data)
        try:
            self.username = data["username"]
            self.email = data["email"]
            self.password = data["password"]
            self.date_joined = None
            date_joined = data.get("date_joined")
            if date_joined:
                self.date_joined = date_joined
            else:
                self.date_joined = date.today()
        except KeyError as error:
            raise models.DataValidationError("Invalid User: missing " + error.args[0]) from error
        except TypeError as error:
            raise models.DataValidationError(
                "Invalid User: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    @classmethod
    def create_model(cls):
        return User()
