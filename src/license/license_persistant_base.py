import os
import secrets

import hashids
import string
import jwt
from bson import ObjectId
from dateutil.relativedelta import relativedelta

from db import db
from src.common.utils import logger
from datetime import datetime, timedelta


class LicensePersistentBase:
    """
    Base class added persistent methods
    """

    def create(self):
        """
        Creates a handshakes in the database
        """
        logger.info("Creating license in subscription= %s", self.gym_id)
        self.generate_product_key()
        self.subscribe_end_date = self.subscribe_date + relativedelta(months=self.period)
        self.subscribe_end_date = self.subscribe_end_date.replace(day=5)
        licenses = db.licenses.insert_one(self.serialize_to_db_without_token())
        self._id = licenses.inserted_id
        self.generate_token()
        licenses = db.licenses
        res = licenses.update_one(
            {'_id': self._id},
            {'$set': self.serialize_to_db()}
        )

        logger.info("license %s Created successfully", self.gym_id)

    def update(self):
        """
        Updates a license to the database
        """
        logger.info("Updating licenses: %s", self._id)
        self.generate_token()
        self.generate_product_key()
        self.subscribe_end_date = self.subscribe_date + relativedelta(months=self.period)
        self.subscribe_end_date = self.subscribe_end_date.replace(day=5)
        licenses = db.licenses
        res = licenses.update_one(
            {'_id': self._id},
            {'$set': self.serialize_to_db()}
        )
        if res.modified_count == 1:
            logger.info("licenses %s Updated successfully", self._id)
        else:
            logger.info("licenses %s could NOT be Updated ", self._id)

    def disable_product_key(self):
        """
        Updates a license to the database
        """
        logger.info("Updating licenses: %s", self._id)
        licenses = db.licenses
        res = licenses.update_one(
            {'_id': self._id},
            {'$set': {'product_key': None}}
        )
        if res.modified_count == 1:
            logger.info("licenses %s Updated successfully", self._id)
        else:
            logger.info("licenses %s could NOT be Updated ", self._id)

    def generate_token(self):
        """generate token key for users"""
        token = jwt.encode(payload={
            'public_id': str(self._id),
            'exp': self.subscribe_end_date
        }, key=os.environ['SECRET_KEY'], algorithm="HS256")

        self.token = token
        return self.token

    def generate_product_key(self):
        """generate token key for users"""
        hashid = hashids.Hashids(salt=os.environ['SECRET_KEY'], min_length=16,
                                 alphabet=string.ascii_uppercase + string.digits)
        value1 = [ord(char) for char in str(self.gym_id)]
        value2 = [ord(char) for char in str(self.plan_id)]
        unique_id = hashid.encode(*value1)

        characters = string.ascii_uppercase + string.digits
        product_key = ''.join(secrets.choice(characters) for _ in range(16))
        formatted_key = '-'.join(product_key[i:i + 4] for i in range(0, len(product_key), 4))
        self.product_key = formatted_key

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all licenses records")
        licenses = db.licenses.find()
        data = []
        if licenses is not None:
            for val in licenses:
                if val is not None:
                    gym_license = cls.create_model()
                    gym_license.deserialize_from_data_base(val)
                    data.append(gym_license)
        return data

    @classmethod
    def all_license(cls, gym_id):
        """Returns all the records in the database"""
        logger.info("Processing all licenses records")

        licenses = db.licenses.find({'gym_id': gym_id})
        data = []
        if licenses is not None:
            for val in licenses:
                if val is not None:
                    gym_license = cls.create_model()
                    gym_license.deserialize_from_data_base(val)
                    data.append(gym_license)
        return data

    @classmethod
    def check_if_exist(cls, gym_id, plan_id, subscription_date):
        """check if record is exist in database"""
        logger.info("check if data exist")
        licenses = db.licenses.find_one({"gym_id": gym_id, "plan_id": plan_id,
                                         "subscribe_date": {"$gte": subscription_date},
                                         "subscribe_end_date": {"$lte": subscription_date}})
        if licenses is not None:

            return True
        return False

    @classmethod
    def find(cls, _id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", _id)
        obj_id = ObjectId(_id)
        licenses = db.licenses.find_one({'_id': obj_id})
        if licenses is not None:
            gym_licenses = cls.create_model()
            gym_licenses.deserialize_from_data_base(licenses)
            return gym_licenses
        return None

    @classmethod
    def find_by_product_key(cls, product_key):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", product_key)
        licenses = db.licenses.find_one({'product_key': product_key})
        if licenses is not None:
            gym_licenses = cls.create_model()
            gym_licenses.deserialize_from_data_base(licenses)
            return gym_licenses
        return None
