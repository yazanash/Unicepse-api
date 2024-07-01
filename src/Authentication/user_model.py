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
                 date_joined=None,
                 notify_token=None,
                 user_type=None,
                 is_verified=None,
                 ):
        super().__init__()
        self.uid = uid
        self.username = username
        self.email = email
        self.password = password
        self.token = token
        self.date_joined = date_joined
        self.notify_token = notify_token
        self.user_type = user_type
        self.is_verified = is_verified
    dt_name = "user"

    def serialize(self):
        """Serializes a User into a dictionary"""
        return {
            'uid': str(self.uid),
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'date_joined': self.date_joined,
            'notify_token': self.notify_token,
            'is_verified': self.is_verified,
            'user_type': self.user_type,
            'token': self.token,
        }

    def secret_serialize(self):
        """Serializes a User into a dictionary"""
        return {
            'uid': str(self.uid),
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined,
            'is_verified': self.is_verified,
            'user_type': self.user_type,
        }

    def deserialize(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.username = data["username"]
            self.email = data["email"]
            self.password = data["password"]
            self.notify_token = data["notify_token"]
            # self.is_verified = data["is_verified"]
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

    def deserialize_update(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.username = data["username"]
            self.notify_token = data["notify_token"]
        except KeyError as error:
            raise models.DataValidationError("Invalid User: missing " + error.args[0]) from error
        except TypeError as error:
            raise models.DataValidationError(
                "Invalid User: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    def deserialize_from_db(self, data):
        """
        Deserializes a User from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        # print(data)
        try:
            self.uid = data.get("_id")
            self.username = data["username"]
            self.email = data["email"]
            self.password = data["password"]
            self.notify_token = data["notify_token"]
            self.token = data["token"]
            self.is_verified = data["is_verified"]
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
