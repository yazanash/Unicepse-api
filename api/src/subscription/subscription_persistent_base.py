import logging
import src.common.errors as err
from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads


class SubscriptionPersistentBase:
    """Base class added persistent methods"""
    dt_name = "Subscriptions"

    def create(self):
        """Creates a Subscription in the database"""

        logger.info("Creating Subscription: %s", self.id)

        subs_ref = db.subscriptions
        subs_ref.insert_one(self.serialize())
        logger.info("Subscription %s Created successfully", self.id)

    def update(self):
        """Updates a Subscription in the database"""

        logger.info("Updating %s", self.id)

        subs_ref = db.subscriptions
        res = subs_ref.update_one({"id": self.id, "gym_id": self.gym_id,"pid": self.pid},
                                  {"$set": self.serialize()})
        if res is not None:
            logger.info("Updated Successfully...")
        else:
            logger.error("Error on Update Subscription:: record may be missing or something else happened!!!...")

    @classmethod
    def all(cls, gym_id, pid):
        """Returns all the records of Subscription in the database"""

        logger.info("Processing all Player-Subscription records")

        subs_ref = db.subscriptions.find({"pid": pid, "gym_id": gym_id})
        data = []
        if subs_ref is not None:
            for val in subs_ref:
                subs = cls.create_model()
                subs.deserialize(val)
                data.append(subs)
        return data

    @classmethod
    def check_if_exist(cls, gym_id, pid, id):
        """check if record is exist in database"""
        logger.info("check if data exist")
        print("if exists called")
        subs_ref = db.subscriptions.find_one({"pid": pid, "gym_id": gym_id, "id": id})
        print(subs_ref)
        if subs_ref is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id, pid, by_uid):
        """Finds a record by its ID"""

        logger.info("Processing lookup for id %s ...", by_uid)

        res = db.subscriptions.find_one({"pid": pid, "gym_id": gym_id, "id": by_uid})
        if res is not None:
            subs = cls.create_model()
            subs.deserialize(res)
            return subs

        return None
