import json
import logging

from bson import ObjectId
from flask import jsonify

from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads


class PlanPersistentBase:
    """
    Base class added persistent methods
    """

    def create(self):
        """
        Creates a gym in the database
        """
        logger.info("Creating plan  %s", self.plan_name)

        plan = db.plans.insert_one(self.serialize_to_data_base())
        self.id = plan.inserted_id
        logger.info("plan %s Created successfully", self.plan_name)

    def update(self):
        """
        Updates a gym to the database
        """
        logger.info("Updating plan: %s", self.plan_name)
        gyms = db.plans
        res = gyms.update_one(
            {"_id": self.id},
            {'$set': self.serialize()}
        )
        if res.modified_count == 1:
            logger.info("gym: %s Updated successfully", self.plan_name)
        else:
            logger.info("gym: %s could NOT be Updated ", self.plan_name)

    @classmethod
    def all(cls):
        """Returns all the records in the database"""
        logger.info("Processing all plans records")
        plans = db.plans.find()
        data = []
        if plans is not None:
            for val in plans:
                if val is not None:
                    plan = cls.create_model()
                    plan.deserialize_from_database(val)
                    data.append(plan)
        return data

    @classmethod
    def check_if_exist(cls, plan_name):
        """check if record is exist in database"""
        logger.info("check if data exist")
        plan = db.plans.find_one({"plan_name": plan_name})
        if plan is not None:
            return True
        return False

    @classmethod
    def find(cls, plan_id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", plan_id)
        plans = db.plans.find_one({'_id': ObjectId(plan_id)})
        if plans is not None:
            plan = cls.create_model()
            plan.deserialize_from_database(plans)
            return plan
        return None
