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
class ProfileService:
    """Base class added persistent methods"""

    def create(self):
        """
        Creates an Account to the database
        """
        logger.info("Creating %s", self.full_name)
        self.level=0
        profile = db.profiles.insert_one(self.serialize())
        logger.info("Successfully created new user %s", self.uid)

    def update(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating %s", self.uid)
        user = db.profiles.update_one({'uid': str(self.uid)},
                                      {'$set': self.serialize()})
        return self

    def update_level(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating %s", self.uid)
        user = db.profiles.update_one({'uid': str(self.uid)},
                                      {'$set': {"level": self.level}})
        return self

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all records")
        data = []
        for item in db.profiles.find():
            profile = cls.create_model()
            data.append(profile.deserialize_from_database(item))
        return data

    @classmethod
    def check_if_exist(cls, uid):
        logger.info("Processing lookup profile id %s ...", uid)
        data = db.profiles
        profile_data = data.find_one({"uid": uid})
        if profile_data is not None:
            return True
        return False

    @classmethod
    def find(cls, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        try:
            data = db.profiles.find_one({"uid": str(by_uid)})
            if data is not None:
                profile = cls.create_model()
                profile.deserialize_from_database(data)
                return profile
            else:
                return None
        except ProfileNotFoundError:
            return None


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class ProfileNotFoundError(Exception):
    """Used for auth validation errors """


class PersistentBase:
    """Used for auth validation errors """
