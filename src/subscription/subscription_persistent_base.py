import logging
import src.common.errors as err
from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads


"""
SNode = Static Node

Map:    ( Standard Model ) 

    Gyms: (SNode)
        gym_id:
            Players: (SNode)
                pl_id:
                    Subs: (SNode)
                        sub_id: 
                            Payments: (SNode)
                                pay_id: VALUE
                    Metrics:
                        list[Metric],
                        

###############################################


Map:    ( Modified Model )

    Gyms:
        (gym_id):
            Players:
                (pl_id),
            Subs:
                (pl_id):
                    (sub_id):
                        Payments:
                            ...data
            
            Metrics:
                (pl_id):
                    (metric_id):
                        ...data

"""


class SubscriptionPersistentBase:
    """Base class added persistent methods"""
    dt_name = "Subscriptions"

    def create(self):
        """Creates a Subscription in the database"""

        logger.info("Creating Subscription: %s", self.id)

        subs_ref = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Subs"]
        res = subs_ref.find({"id": self.id})
        res = loads(dumps(res))

        if len(res) == 0:
            subs_ref.insert_one(self.serialize())
            logger.info("Subscription %s Created successfully", self.id)
        else:
            logger.error("Error in Subscription: %s", self.id)
            raise err.DuplicateRecordError()

    def update(self):
        """Updates a Subscription in the database"""

        logger.info("Updating %s", self.id)

        subs_ref = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Subs"]
        res = subs_ref.update_one({"id": self.id}, {"$set": self.serialize()})
        if res is not None:
            logger.info("Updated Successfully...")
        else:
            logger.error("Error on Update Subscription:: record may be missing or something else happened!!!...")

    def delete(self):
        """Removes a Subscription from the data store"""
        logger.info("Deleting %s", self.id)

        subs_ref = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Subs"]
        res = subs_ref.delete_one({"id": self.id})
        if res.deleted_count == 1:
            logger.info("Subscription %s Deleted successfully", self.id)
        else:
            raise FileNotFoundError

    @classmethod
    def all(cls, gym_id, pl_id):
        """Returns all the records of Subscription in the database"""

        logger.info("Processing all Player-Subscription records")

        subs_ref = db["Gyms"][gym_id]["Players"][pl_id]["Subs"].find()
        data = []
        all_subs = loads(dumps(subs_ref))
        if all_subs is not None:
            for val in all_subs:
                if val is not None:
                    subs = cls.deserialize(val)
                    data.append(subs)
        return data

    @classmethod
    def all_json(cls, pl_id):
        """Returns all the records of Subscription in the database"""

        logger.info("Processing all Player-transaction records")

        subs_ref = db["Gyms"][cls.gym_id]["Players"][pl_id]["Subs"].find()
        json_subs = loads(dumps(subs_ref))
        if json_subs is not None:
            logger.info("Fetching Player %s Subscriptions as Json", pl_id)
            return json_subs
        return []

    @classmethod
    def check_if_exist(cls, gym_id, pl_id, uid):
        """check if record is exist in database"""
        logger.info("check if data exist")

        subs_ref = db["Gyms"][gym_id]["Players"][pl_id]["Subs"].find({"id": uid})
        if subs_ref is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id, pl_id, by_uid):
        """Finds a record by its ID"""

        logger.info("Processing lookup for id %s ...", by_uid)

        res = db["Gyms"][gym_id]["Players"][pl_id]["Subs"].find_one({"id": by_uid})
        subs_ref = loads(dumps(res))
        if subs_ref is not None:
            subs = cls.deserialize(subs_ref)
            return subs

        return None
