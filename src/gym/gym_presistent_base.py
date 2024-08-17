import json
import logging

from bson import ObjectId
from flask import jsonify

from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads


class GymPersistentBase:
    """
    Base class added persistent methods
    """

    def create(self):
        """
        Creates a gym in the database
        """
        logger.info("Creating Gym  %s", self.gym_name)

        gyms = db.gyms.insert_one(self.serialize_to_db())
        self.id = gyms.inserted_id
        logger.info("gym %s Created successfully", self.gym_name)

    def update(self):
        """
        Updates a gym to the database
        """
        logger.info("Updating gym: %s", self.gym_name)
        gyms = db.gyms
        res = gyms.update_one(
            {"id": self.id},
            {'$set': self.serialize()}
        )
        if res.modified_count == 1:
            logger.info("gym: %s Updated successfully", self.gym_name)
        else:
            logger.info("gym: %s could NOT be Updated ", self.gym_name)

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all gyms records")
        gyms = db.gyms.find()
        data = []
        if gyms is not None:
            for val in gyms:
                if val is not None:
                    gym = cls.create_model()
                    gym.deserialize_from_db(val)
                    data.append(gym)
        return data

    @classmethod
    def check_if_exist(cls, gym_name):
        """check if record is exist in database"""
        logger.info("check if data exist")
        gym = db.gyms.find_one({"gym_name": gym_name})
        if gym is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", gym_id)
        obj_id = ObjectId(gym_id)
        gyms = db.gyms.find_one({'_id': obj_id})
        if gyms is not None:
            gym = cls.create_model()
            gym.deserialize_from_db(gyms)
            return gym
        return None
