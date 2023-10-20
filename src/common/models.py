"""
base CRUD Model

"""
import logging
from datetime import date

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

logger = logging.getLogger("flask.app")

cred = credentials.Certificate('platinum-8b28f-firebase-adminsdk-ln291-90678268e5.json')
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://platinum-8b28f-default-rtdb.firebaseio.com"
})
base = db
database = db.reference('test')


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    def create(self):
        """
        Creates an Account to the database
        """
        logger.info("Creating %s", self.username)
        # self.uid = None  # id must be none to generate next primary key
        print(database)
        users_ref = database.child(self.uid)
        users_ref.set(self.serialize())

    def update(self):
        """
        Updates an Account to the database
        """
        logger.info("Updating %s", self.username)

    def delete(self):
        """Removes a Account from the data store"""
        logger.info("Deleting %s", self.username)

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def init_firebase(cls):
        """Finds a record by its ID"""
        logger.info("Initialize firebase database ...")


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""

