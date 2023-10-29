"""
base CRUD Model

"""
import logging
import os

from werkzeug.security import check_password_hash, generate_password_hash
import firebase_admin
from firebase_admin import auth, _auth_utils
import jwt
from datetime import datetime, timedelta

# firebase_admin.initialize_app()
logger = logging.getLogger("flask.app")


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class AuthService:
    """Base class added persistent methods"""

    def create(self):
        """
        Creates an Account to the database
        """
        logger.info("Creating %s", self.email)
        user = auth.create_user(
            email=self.email,
            email_verified=False,
            display_name=self.username,
            password=self.password,
            disabled=False
        )
        self.uid = user.uid
        auth.set_custom_user_claims(self.uid, {
            'Role': 'player',
            'token': self.generate_token(),
            'date_joined': str(self.date_joined)
        })
        logger.info("Successfully created new user %s", self.uid)

    def update(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating %s", self.uid)
        user = auth.update_user(
            self.uid,
            email=self.email,
            email_verified=False,
            password=self.password,
            disabled=False)
        auth.set_custom_user_claims(self.uid, {
            'Role': 'player',
            'token': self.generate_token(),
            'date_joined': str(self.date_joined)
        })
        return self

    def delete(self):
        """Removes a user from the data store"""
        logger.info("Deleting %s", self.username)
        user = auth.delete_user(self.uid)

    def generate_token(self):
        """generate token key for users"""
        token = jwt.encode({
            'public_id': str(self.uid),
            'exp': datetime.utcnow() + timedelta(days=90)
        }, os.environ['SECRET_KEY'])
        self.token = token

    def login_user(self):
        """verify user credentials """

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all records")
        page = auth.list_users()
        data = []
        while page:
            for user in page.users:
                user_data = cls.create_model()
                user_data.uid = user.uid
                user_data.username = user.display_name
                user_data.email = user.email
                if user.custom_claims is not None:
                    user_data.date_joined = user.custom_claims.get('date_joined')
                data.append(user_data)
            # Get next batch of users.
            page = page.get_next_page()
        return data

    @classmethod
    def delete_multi_users(cls, users):
        """Returns all the records in the database"""
        logger.info("Processing delete multi users")
        result = auth.delete_users(users)

    @classmethod
    def check_if_exist(cls, uid):
        """check if record is exist in database"""
        logger.info("check is data exist")
        try:
            data = auth.get_user(uid)
            user = cls.create_model()
            user.uid = data.uid
            user.email = data.email
            return user
        except auth.UserNotFoundError as error:
            raise AuthValidationError(error.args[0]) from error

    @classmethod
    def get_user_by_email(cls, email):
        """check if record is exist in database"""
        logger.info("check is data exist")
        data = auth.get_user_by_email(email)
        user = cls.create_model()
        user.uid = data.uid
        user.email = data.email
        return user

    @classmethod
    def find(cls, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        try:
            data = auth.get_user(str(by_uid))
            user = cls.create_model()
            user.uid = data.uid
            user.username = data.display_name
            user.email = data.email
            user.date_joined = data.custom_claims.get('date_joined')
            return user
        except _auth_utils.UserNotFoundError as error:
            return None


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class AuthValidationError(Exception):
    """Used for auth validation errors """


class PersistentBase():
    """Used for auth validation errors """
