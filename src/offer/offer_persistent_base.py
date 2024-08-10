import json
import logging

from bson import ObjectId
from flask import jsonify

from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads


class OfferPersistentBase:
    """
    Base class added persistent methods
    """

    def create(self):
        """
        Creates an offer in the database
        """
        logger.info("Creating offer  %s", self.offer_name)

        offers = db.offers.insert_one(self.serialize_to_data_base())
        self.id = offers.inserted_id
        logger.info("offer %s Created successfully", self.offer_name)

    def update(self):
        """
        Updates an offer to the database
        """
        logger.info("Updating offer: %s", self.offer_name)
        offers = db.offers
        res = offers.update_one(
            {"_id": self.id},
            {'$set': self.serialize()}
        )
        if res.modified_count == 1:
            logger.info("offer: %s Updated successfully", self.offer_name)
        else:
            logger.info("offer: %s could NOT be Updated ", self.offer_name)

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all offer records")
        offers = db.offers.find()
        data = []
        if offers is not None:
            for val in offers:
                if val is not None:
                    offer = cls.create_model()
                    offer.deserialize_from_database(val)
                    data.append(offer)
        return data

    @classmethod
    def check_if_exist(cls, offer_name):
        """check if record is exist in database"""
        logger.info("check if data exist")
        offer = db.offers.find_one({"offer_name": offer_name})
        if offer is not None:
            return True
        return False

    @classmethod
    def find(cls, offer_id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", offer_id)
        offers = db.offers.find_one({'_id': ObjectId(offer_id)})
        if offers is not None:
            offer = cls.create_model()
            offer.deserialize_from_database(offers)
            return offer
        return None
