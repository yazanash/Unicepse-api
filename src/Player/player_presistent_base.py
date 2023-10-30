import logging
from firebase_admin import db
from src.common.utils import logger


class PlayerPersistentBase:
    """Base class added persistent methods"""
    dt_name = "players"
    players_table = "players_table"

    def create(self):
        """
        Creates a Player to the database
        """
        logger.info("Creating %s", self.name)
        # self.uid = None  # id must be none to generate next primary key
        players_ref = db.reference(self.dt_name).child(self.players_table).child(str(self.pid))
        players_ref.set(self.serialize())
        logger.info("Created %s successfully", self.name)

    def update(self):
        """
        Updates a Player to the database
        """
        logger.info("Updating %s", self.name)
        players_ref = db.reference(self.dt_name).child(self.players_table).child(str(self.pid))
        players_ref.update(self.serialize())

    def delete(self):
        """Removes a Player from the data store"""
        logger.info("Deleting %s", self.name)
        db.reference(self.dt_name).child(self.players_table).child(str(self.pid)).delete()

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all Player records")
        player_ref = db.reference(cls.dt_name).child(cls.players_table).get()
        print(player_ref)
        data = []
        print(type(player_ref))
        if player_ref is not None:
            for key, val in player_ref.items():
                user = cls.create_model()
                user.deserialize(val)
                data.append(user)
        return data

    @classmethod
    def check_if_exist(cls, uid):
        """check if record is exist in database"""
        logger.info("check if data exist")
        player_ref = db.reference(cls.dt_name).child(cls.players_table).child(str(uid)).get()
        print("player ref in check if exist: ", player_ref)
        if player_ref is not None:
            return True

        return False

    @classmethod
    def find(cls, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        players_ref = db.reference(cls.dt_name).child(cls.players_table).child(str(by_uid))
        if players_ref.get() is not None:

            player = cls.deserialize(players_ref.get())
            return player

        return None


