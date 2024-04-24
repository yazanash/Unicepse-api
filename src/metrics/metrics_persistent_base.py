from db import db
from src.common.utils import logger
from src.common import errors
from bson.json_util import loads, dumps


class MetricPersistentBase:

    def create(self):
        """Creates New Metric for player in db"""
        logger.info("creating new metric for player %s", self.pl_id)

        metrics_ref = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Metrics"]
        print("metrics_ref: ",metrics_ref)

        if len(loads(dumps(metrics_ref.find({"id": self.id})))) == 0:
            metrics_ref.insert_one(self.serialize())
            logger.info("Successful creation of metric: %s", self.id)

        else:
            logger.error("Duplicate data ERR found: %s", self.serialize())
            raise errors.DuplicateRecordError()

    def update(self):
        """Updates a Metric for player in db"""
        logger.info("Updating Metric for player: %s", self.pl_id)

        metrics_ref = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Metrics"]
        res = metrics_ref.update_one({"id": self.id}, {"$set": self.serialize()})

        if res.modified_count == 1:
            logger.info("Successfully Updated: %s", self.id)
        else:
            logger.error("No Metric Record found for id: %s", self.id)

    def delete(self):
        """Deletes a Metric for player in db"""
        logger.info("Deleting Metric for player: %s", self.pl_id)

        metrics_ref = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Metrics"]
        res = metrics_ref.delete_one({"id": self.id})

        if res.deleted_count == 1:
            logger.info("Successfully Deleted Record: %s", self.id)
        else:
            logger.error("Unable to Delete record: %s",self.id)

    @classmethod
    def all(cls, gym_id, pl_id):
        """Returns all Records of Player Metrics"""
        logger.info("Fetching all player metric Records")

        metrics_ref = db["Gyms"][gym_id]["Players"][pl_id]["Metrics"].find()
        metrics = loads(dumps(metrics_ref))
        res = []

        for i in metrics:
            logger.info("deserializing all metric records for player: %s", pl_id)
            res.append(cls.deserialize(i))

        return res

    @classmethod
    def all_json(cls, gym_id, pl_id):
        """Returns all Records in Json Format"""
        logger.info("Fetching all player metric Records")

        metrics_ref = db["Gyms"][gym_id]["Players"][pl_id]["Metrics"].find()
        if len(metrics_ref) > 0:
            return dumps(metrics_ref)

    @classmethod
    def check_if_exist(cls, gym_id, pl_id, met_id):
        """Checks if record exists in DB"""
        logger.info("Checking if metric %s exists", met_id)

        metric = db["Gyms"][gym_id]["Players"][pl_id]["Metrics"].find_one({"id", met_id})
        if metric is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id, pl_id, met_id):
        """Finds a record in DB"""
        logger.info("Searching for Metric= %s, Player= %s, Gym= %s", met_id, pl_id, gym_id)
        metrics_res = db["Gyms"][gym_id]["Players"][pl_id]["Metrics"].find_one({"id": met_id})
        if metrics_res is not None:
            logger.info("Found! : %s", met_id)
            return metrics_res
        else:
            logger.error("Not Found! : %s", met_id)
            return None
