from db import db
from src.common.utils import logger
from src.common import errors
from bson.json_util import loads, dumps


class MetricPersistentBase:

    def create(self):
        """Creates New Metric for player in db"""
        logger.info("creating new metric for player %s", self.pid)

        metrics_ref = db.metrics
        metrics_ref.insert_one(self.serialize())
        logger.info("Successful creation of metric: %s", self.id)

    def update(self):
        """Updates a Metric for player in db"""
        logger.info("Updating Metric for player: %s", self.pid)

        metrics_ref = db.metrics
        res = metrics_ref.update_one({"id": self.id, "pid": self.pid, "gym_id": self.gym_id},
                                     {"$set": self.serialize()})
        logger.info("Successfully Updated: %s", self.id)

    @classmethod
    def all(cls, gym_id, pid):
        """Returns all Records of Player Metrics"""
        logger.info("Fetching all player metric Records")

        metrics_ref = db.metrics.find({"pid": int(pid), "gym_id": int(gym_id)})
        res = []

        for i in metrics_ref:
            logger.info("deserializing all metric records for player: %s", pid)
            metric = cls.create_model()
            metric.deserialize(i)
            res.append(metric)

        return res

    @classmethod
    def check_if_exist(cls, gym_id, pid, id):
        """Checks if record exists in DB"""
        logger.info("Checking if metric %s exists", id)
        metric = db.metrics.find_one({"id": id, "pid": pid, "gym_id": gym_id})
        print(metric)
        if metric is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id, pid, id):
        """Finds a record in DB"""
        logger.info("Searching for Metric= %s, Player= %s, Gym= %s", id, pid, gym_id)
        metrics_res = db.metrics.find_one({"id": id, "pid": pid, "gym_id": gym_id})
        if metrics_res is not None:
            metrics = cls.create_model()
            metrics.deserialize(metrics_res)
            return metrics
        else:
            return None
