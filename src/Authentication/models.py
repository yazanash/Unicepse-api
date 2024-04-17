"""
base CRUD Model

"""
import base64
import hashlib
import logging
import os

import pyotp

# from app import mail
# from flask_mail import Mail, Message
from bson import ObjectId
from flask import Flask, current_app
from flask_mail import Message, Mail
from werkzeug.security import check_password_hash, generate_password_hash
import firebase_admin
from firebase_admin import auth, _auth_utils
import jwt
from datetime import datetime, timedelta
from db import db
from app import mail
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
        self.password = generate_password_hash(self.password)
        user = db.Users.insert_one(self.serialize())

        self.uid = user.inserted_id
        logger.info("Successfully created new user %s", self.uid)

    def update(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating %s", self.uid)
        self.password = generate_password_hash(self.password)
        user = db.Users.update_one({'_id': ObjectId(self.uid)},
                                   {'$set': self.serialize()})

        return self

    def delete(self):
        """Removes a user from the data store"""
        logger.info("Deleting %s", self.username)
        user = auth.delete_user(self.uid)

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
        print(credentials)
        print(self.password)
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
    def delete_multi_users(cls, users):
        """Returns all the records in the database"""
        logger.info("Processing delete multi users")
        result = auth.delete_users(users)
        print(len(users))

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
        data = db.Users.find_one({"email": email})
        user = cls.create_model()
        user.deserialize_from_db(data)
        # print(user.password)
        return user

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
        except _auth_utils.UserNotFoundError as error:
            return None

    @classmethod
    def send_email(cls, email):
        """Finds a record by its ID"""
        logger.info("Processing send verify email for email %s ...", email)
        print(email)
        asd = current_app.app_context()
        msg = Message('Hello From Unicepse', sender='unicepse@gmail.com',
                      recipients=[email])
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp = totp.now()
        print(otp)
        # print(mail)
        msg.body = f"Hello From unicepse this email is a test this is your otp {otp}"
        with current_app.app_context():
            msg = Message("Hello",
                          sender="from@example.com",
                          recipients=[email])
            msg.body = "This is a test email from our Flask app."
            mail.send(msg)
        # print(mail)
        db.emails.insert_one({email: otp})


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class AuthValidationError(Exception):
    """Used for auth validation errors """


class PersistentBase():
    """Used for auth validation errors """
