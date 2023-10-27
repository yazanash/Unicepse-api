"""
base CRUD Model

"""
import logging
from datetime import date
from firebase_admin import exceptions

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import os



logger = logging.getLogger("flask.app")

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://platinum-8b28f-default-rtdb.firebaseio.com"
})
base = db


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class added persistent methods"""
    dt_name = "user"

    def create(self):
        """
        Creates an Account to the database
        """
        logger.info("Creating %s", self.username)
        # self.uid = None  # id must be none to generate next primary key
        users_ref = db.reference(self.dt_name).child(str(self.uid))
        users_ref.set(self.serialize())
        logger.info("Created %s successfully", self.username)

    def update(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating %s", self.username)
        users_ref = db.reference(self.dt_name).child(str(self.uid))
        users_ref.update(self.serialize())

    def delete(self):
        """Removes a user from the data store"""
        logger.info("Deleting %s", self.username)
        users_ref = db.reference(self.dt_name).child(str(self.uid)).delete()

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all records")
        user_ref = db.reference(cls.dt_name).get()
        print(user_ref)
        data = []
        print(type(user_ref))
        if user_ref is not None:
            for key, val in user_ref.items():
                user = cls.create_model()
                user.deserialize(val)
                data.append(user)
        return data

    @classmethod
    def check_if_exist(cls, uid):
        """check if record is exist in database"""
        logger.info("check is data exist")
        user_ref = db.reference(cls.dt_name).child(str(uid)).get()
        if user_ref is not None:
            user = cls.create_model()
            user.deserialize(user_ref)
            return user
        else:
            return None

    @classmethod
    def find(cls, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        users_ref = db.reference(cls.dt_name).child(str(by_uid))
        if users_ref.get() is not None:
            user = cls.create_model()
            user.deserialize(users_ref.get())
            return user
        else:
            return None


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""

