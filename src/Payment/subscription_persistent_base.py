import logging
from firebase_admin import db
from src.common.utils import logger


class SubscriptionPersistentBase:
    """Base class added persistent methods"""
    dt_name = "Subscriptions"

    def create(self):
        """
        Creates a Player to the database
        """
        logger.info("Creating %s", self.id)
        # self.uid = None  # id must be none to generate next primary key
        subs_ref = db.reference(self.dt_name).child(str(self.pl_id)).child(str(self.id))
        subs_ref.set(self.serialize())
        logger.info("Created %s successfully", self.id)

    def update(self):
        """
        Updates a Player to the database
        """
        logger.info("Updating %s", self.id)
        subs_ref = db.reference(self.dt_name).child(str(self.pl_id)).child(str(self.id))
        subs_ref.update(self.serialize())

    def delete(self):
        """Removes a Player from the data store"""
        logger.info("Deleting %s", self.id)
        db.reference(self.dt_name).child(self.pl_id).child(str(self.id)).delete()

    @classmethod
    def all(cls, pl_id):
        """Returns all the records in the database"""
        logger.info("Processing all Player-transaction records")
        player_ref = db.reference(cls.dt_name).child(str(pl_id)).get()
        print(player_ref)
        data = []
        print(type(player_ref))
        if player_ref is not None:
            for val in player_ref:
                if val is not None:
                    print("Val in ref: ", type(val))
                    subs = cls.deserialize(val)
                    data.append(subs)
        return data

    @classmethod
    def check_if_exist(cls, pl_id,uid):
        """check if record is exist in database"""
        logger.info("check if data exist")
        subs_ref = db.reference(cls.dt_name).child(str(pl_id)).child(str(uid)).get()
        print("player ref in check if exist: ", subs_ref)
        if subs_ref is not None:
            return True

        return False

    @classmethod
    def find(cls, player_id, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        subs_ref = db.reference(cls.dt_name).child(str(player_id)).child(str(by_uid))
        if subs_ref.get() is not None:
            player = cls.deserialize(subs_ref.get())
            return player

        return None
