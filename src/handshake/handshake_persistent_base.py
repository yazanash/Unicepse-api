import datetime
import json
import logging

from firebase_admin.messaging import UnregisteredError
from flask import jsonify

import firebase_helper
from src.Authentication.profile_model import Profile
from src.Authentication.user_model import User
from src.attedence.attendance_model import Attendance
from src.metrics.metrics_model import Metric
from src.common import points, notification_messages
from src.routine.routine_model import Routine
from src.subscription.subscription_model import Subscription
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
        self.created_at = datetime.datetime.now(datetime.timezone.utc)
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

    def delete(self):
        """
        Updates a handshakes to the database
        """
        logger.info("Updating handshake: %s", self.pid)

        handshakes = db.handshakes
        res = handshakes.delete_one({'uid': self.sid,'pid': self.pid, "gym_id": self.gym_id})
        # if res.modified_count == 1:
        #     logger.info("handshake %s Updated successfully", self.pid)
        # else:
        #     logger.info("handshake %s could NOT be Updated ", self.pid)

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
    def all_by_gym(cls, gym_id):
        """Returns all the records in the database"""
        logger.info("Processing all Player-handshakes records")
        handshakes = db.handshakes.find({'gym_id': str(gym_id)})
        data = []
        if handshakes is not None:
            for val in handshakes:
                if val is not None:
                    handshake = cls.create_model()
                    handshake.deserialize_from_db(val)
                    data.append(handshake)
        return data

    @classmethod
    def check_if_exist(cls, gym_id, uid):
        """check if record is exist in database"""
        logger.info("check if data exist")
        handshake = db.handshakes.find_one({"gym_id": gym_id, "uid": uid})
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

    @classmethod
    def find_by_player(cls, gym_id, pid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", pid)
        handshakes = db.handshakes.find_one({'pid': str(pid), "gym_id": str(gym_id)})
        if handshakes is not None:
            handshake = cls.create_model()
            handshake.deserialize_from_db(handshakes)
            return handshake
        return None

    def set_level(self):
        """Finds a record by its ID"""
        subs = Subscription.all(self.gym_id, self.pid)
        routines = Routine.all(self.gym_id, self.pid)
        metrics = Metric.all(self.gym_id, self.pid)
        attendances = Attendance.all(self.pid, self.gym_id)
        po = 0
        po += len(subs) * points.SUBSCRIPTION_POINTS
        po += len(routines) * points.ROUTINE_POINTS
        po += len(metrics) * points.METRIC_POINTS
        po += len(attendances) * points.ATTENDANCES_POINTS
        profile = Profile.find(self.uid)
        if profile is not None:
            profile.level += po
            profile.update_level()

    def set_single_level(self, point):
        """Finds a record by its ID"""
        profile = Profile.find(self.uid)
        if profile is not None:
            profile.level += point
            profile.update_level()

    def send_notification(self, title, body):
        """
        Updates an Account to the database
        """
        try:
            user = User.find(self.uid)
            firebase_helper.send_notification(user.notify_token, title, body)
        except UnregisteredError as ex:
            return ex
