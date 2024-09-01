import datetime
import json
import logging

from flask import jsonify

from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads


class HandShakePersistentBase:
    """
    Base class added persistent methods
    """

    def create(self):
        """
        Creates a handshakes in the database
        """
        logger.info("Creating Payment in subscription= %s", self.pid)
        self.status = True
        self.created_at = datetime.datetime.now()
        handshakes = db.handshakes
        handshakes.insert_one(self.serialize())

        logger.info("handshake %s Created successfully", self.pid)

    def update(self):
        """
        Updates a handshakes to the database
        """
        logger.info("Updating handshake: %s", self.pid)
        self.status = True
        self.created_at = datetime.datetime.now()
        handshakes = db.handshakes
        res = handshakes.update_one(
            {'uid': self.sid,'pid': self.pid, "gym_id": self.gym_id},
            {'$set': self.serialize()}
        )
        if res.modified_count == 1:
            logger.info("handshake %s Updated successfully", self.pid)
        else:
            logger.info("handshake %s could NOT be Updated ", self.pid)

    @classmethod
    def all(cls, uid):
        """Returns all the records in the database"""
        logger.info("Processing all Player-handshakes records")
        handshakes = db.handshakes.find({'uid': str(uid)})
        data = []
        if handshakes is not None:
            for val in handshakes:
                if val is not None:
                    handshake = cls.create_model()
                    handshake.deserialize_from_db(val)
                    data.append(handshake)
        return data

    @classmethod
    def check_if_exist(cls, gym_id, uid, pid ):
        """check if record is exist in database"""
        logger.info("check if data exist")
        handshake = db.handshakes.find_one({"gym_id": gym_id, "pid": pid, "uid": uid})
        if handshake is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id, pid, uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", uid)
        handshakes = db.handshakes.find_one({'uid': uid, 'pid': pid, "gym_id": gym_id})
        if handshakes is not None:
            handshake = cls.create_model()
            handshake.deserialize_from_db(handshakes)
            return handshake
        return None

    @classmethod
    def find_single(cls, uid, gym_id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", uid)
        handshakes = db.handshakes.find_one({'uid': str(uid), "gym_id": str(gym_id)})
        if handshakes is not None:
            handshake = cls.create_model()
            handshake.deserialize_from_db(handshakes)
            return handshake
        return None
