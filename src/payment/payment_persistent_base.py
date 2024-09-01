import json
import logging

from flask import jsonify

from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads


class PaymentPersistentBase:
    """
    Base class added persistent methods
    """

    def create(self):
        """
        Creates a Payment in the database
        """
        logger.info("Creating Payment in subscription= %s", self.sid)

        payments = db.payments
        payments.insert_one(self.serialize())
        # payments.insert_one(self.serialize())

        logger.info("Payment %s Created successfully", self.sid)

    def update(self):
        """
        Updates a Player to the database
        """
        logger.info("Updating Payment: %s", self.id)

        payments = db.payments
        res = payments.update_one(
            {'sid': self.sid,'pid': self.pid, "gym_id": self.gym_id, "id": self.id},
            {'$set': self.serialize()}
        )
        # res = payments.update_one({"id": self.id}, {"$set": self.serialize()})
        if res.modified_count == 1:
            logger.info("Payment %s Updated successfully", self.id)
        else:
            logger.info("Payment %s could NOT be Updated ", self.id)

    def delete(self):
        """Removes a Player from the data store"""
        logger.info("Deleting %s", self.id)

        payments = db.payments

        res = payments.delete_one(
            {'id': self.id,'sid': self.sid, 'pid': self.pid, "gym_id": self.gym_id}
        )

        # res = payments.delete_one({"id": self.id})

        logger.info("Payment %s Deleted successfully", self.id)

    @classmethod
    def all(cls, gym_id, pid, sid):
        """Returns all the records in the database"""
        logger.info("Processing all Player-transaction records")
        payments = db.payments.find({'sid': sid, 'pid': pid, "gym_id": gym_id})
        data = []
        if payments is not None:
            for val in payments:
                if val is not None:
                    payment = cls.create_model()
                    payment.deserialize(val)
                    data.append(payment)
        return data

    @classmethod
    def check_if_exist(cls, gym_id, pid, sid, id):
        """check if record is exist in database"""
        logger.info("check if data exist")

        payment = db.payments.find_one({"gym_id": gym_id, "pid": pid, "id": sid, "id": id})
        if payment is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id, pid, sid, id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", id)
        payment = db.payments.find_one({'id': id, 'sid': sid, 'pid': pid, "gym_id": gym_id})
        if payment is not None:
            pay = cls.create_model()
            pay.deserialize(payment)
            return pay
        return None
