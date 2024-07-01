"""
base CRUD Model

"""
import logging
import os
import pyotp
from bson import ObjectId
from flask import current_app
from flask_mail import Message, Mail
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from datetime import datetime, timedelta

from db import db
# from app import mail
from mail import mail
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
        self.password = generate_password_hash(self.password)
        user = db.Users.insert_one(self.serialize())

        self.uid = user.inserted_id
        logger.info("Successfully created new user %s", self.uid)

    def update(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating %s", self.uid)
        user = db.Users.update_one({'_id': ObjectId(self.uid)},
                                   {'$set': self.serialize()})
        return self

    def update_password(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating password %s", self.uid)
        self.password = generate_password_hash(self.password)
        user = db.Users.update_one({'_id': ObjectId(self.uid)},
                                   {'$set': self.serialize()})
        return self

    def generate_token(self):
        """generate token key for users"""
        token = jwt.encode(payload={
            'public_id': str(self.uid),
            'exp': datetime.utcnow() + timedelta(days=90)
        }, key=os.environ['SECRET_KEY'], algorithm="HS256")

        self.token = token
        return self.token

    def login_user(self, credentials):
        """verify user credentials """
        if check_password_hash(self.password, credentials['password']):
            return self.generate_token()
        else:
            return None

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all records")
        data = []
        for item in db.Users.find():
            user = cls.create_model()
            data.append(user.deserialize_from_db(item))
        return data

    @classmethod
    def get_user_by_email(cls, email):
        """send email verification to user """
        try:
            logger.info("check is data exist")
            data = db.Users.find_one({"email": email})
            if data is not None:
                user = cls.create_model()
                user.deserialize_from_db(data)
                return user
            else:
                raise UserNotFoundError
        except UserNotFoundError:
            return None

    @classmethod
    def find(cls, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        try:
            if ObjectId.is_valid(by_uid):
                data = db.Users.find_one({"_id": ObjectId(by_uid)})
                user = cls.create_model()
                user.deserialize_from_db(data)
                return user
            else:
                return None
        except UserNotFoundError:
            return None

    @classmethod
    def send_email(cls, email):
        """Finds a record by its ID"""
        logger.info("Processing send verify email for email %s ...", email)

        msg = Message('Hello From Unicepse', sender='unicepse@gmail.com',
                      recipients=[email])
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp = totp.now()

        msg.body = f"Hello From unicepse this email is a test this is your otp {otp}"
        # with current_app.app_context():
        mail.send(msg)
        db.emails.delete_one({"email": email})
        db.emails.insert_one({"email": email, "otp": otp})

    @classmethod
    def verify_otp(cls, email, otp):
        """Finds a record by its ID"""
        logger.info("Processing send verify email for email %s ...", email)
        returned_email = db.emails.find_one({"email": email})
        if returned_email["otp"] == otp:
            return True
        else:
            return False

    @classmethod
    def delete_from_otp(cls, email):
        """Delete email after verifying"""
        logger.info("Processing delete email after verify %s ...", email)
        db.emails.delete_one({"email": email})


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class AuthValidationError(Exception):
    """Used for auth validation errors """


class UserNotFoundError(Exception):
    """Used for auth validation errors """


class PersistentBase:
    """Used for auth validation errors """
