import logging

from bson import ObjectId

from db import db
from src.common.utils import logger

node_name = "players"


class PlayerPersistentBase:
    """Base class added persistent methods"""

    def create(self):
        """
        Creates a Player to the database
        """
        logger.info("Creating %s", self.name)
        player_ref = db.players
        player_ref.insert_one(self.serialize())
        logger.info("Created %s successfully", self.name)

    def update(self):
        """
        Updates a Player to the database
        """
        logger.info("Updating %s", self.name)
        player_ref = db.players
        player_ref.update_one({'pid': self.pid,'gym_id': self.gym_id}, {'$set': self.serialize()})
        logger.info("Updated Successfully %s", self.name)

    @classmethod
    def all(cls, gym_id):
        """Returns all the records in the database"""
        logger.info("Processing all Player records")
        player_ref = db.players
        data = []
        if player_ref is not None:
            for val in player_ref:
                player = cls.create_model()
                player.deserialize(val)
                data.append(player)
        return data

    @classmethod
    def find(cls, gym_id, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        try:
            player_data = db.players.find_one({"pid": by_uid, "gym_id": gym_id})
            if player_data is not None:
                player = cls.create_model()
                player.deserialize(player_data)
                return player
            else:
                return None
        except PlayerNotFoundError:
            return None

    @classmethod
    def check_if_exist(cls, gym_id, by_uid):
        """check if record is exist in database"""
        logger.info("check if data exist")
        print("if exist")
        data = db.players
        player_data = data.find_one({"pid": by_uid, "gym_id": gym_id})
        print(player_data)
        if player_data is not None:
            return True
        return False


class PlayerNotFoundError(Exception):
    """Used for auth validation errors """

