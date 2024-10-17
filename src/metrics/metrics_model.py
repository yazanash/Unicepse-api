from .metrics_persistent_base import MetricPersistentBase
from datetime import datetime


class Metric(MetricPersistentBase):
    def __init__(
            self,
            id=None,
            pid=None,
            gym_id=None,
            height=None,
            weight=None,
            l_arm=None,
            r_arm=None,
            l_humerus=None,
            r_humerus=None,
            l_thigh=None,
            r_thigh=None,
            l_leg=None,
            r_leg=None,
            neck=None,
            shoulders=None,
            waist=None,
            chest=None,
            hips=None,
            check_date=None):
        self.id = id
        self.pid = pid
        self.gym_id = gym_id
        self.height = height
        self.weight = weight
        self.l_arm = l_arm
        self.r_arm = r_arm
        self.l_humerus = l_humerus
        self.r_humerus = r_humerus
        self.l_thigh = l_thigh
        self.r_thigh = r_thigh
        self.l_leg = l_leg
        self.r_leg = r_leg
        self.neck = neck
        self.shoulders = shoulders
        self.waist = waist
        self.chest = chest
        self.hips = hips
        self.check_date = check_date

    def serialize(self):
        return {
            "id": self.id,
            "pid": self.pid,
            "gym_id": self.gym_id,
            "height": self.height,
            "weight": self.weight,
            "l_arm": self.l_arm,
            "r_arm": self.r_arm,
            "l_humerus": self.l_humerus,
            "r_humerus": self.r_humerus,
            "l_thigh": self.l_thigh,
            "r_thigh": self.r_thigh,
            "l_leg": self.l_leg,
            "r_leg": self.r_leg,
            "neck": self.neck,
            "shoulders": self.shoulders,
            "waist": self.waist,
            "chest": self.chest,
            "hips": self.hips,
            "check_date": self.check_date,
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.id = json['id']
        self.pid = json['pid']
        self.gym_id = json['gym_id']
        self.height = json['height']
        self.weight = json['weight']
        self.l_arm = json['l_arm']
        self.r_arm = json['r_arm']
        self.l_humerus = json['l_humerus']
        self.r_humerus = json['r_humerus']
        self.l_thigh = json['l_thigh']
        self.r_thigh = json['r_thigh']
        self.l_leg = json['l_leg']
        self.r_leg = json['r_leg']
        self.neck = json['neck']
        self.shoulders = json['shoulders']
        self.waist = json['waist']
        self.chest = json['chest']
        self.hips = json['hips']
        self.check_date = json['check_date']

    @staticmethod
    def create_model():
        return Metric()
