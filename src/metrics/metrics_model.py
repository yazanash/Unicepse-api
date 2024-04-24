from .metrics_persistent_base import MetricPersistentBase
from datetime import datetime


class Metric(MetricPersistentBase):
    def __init__(
            self,
            id,
            pl_id,
            gym_id,
            height,
            weight,
            l_arm,
            r_arm,
            l_humerus,
            r_humerus,
            l_thigh,
            r_thigh,
            l_leg,
            r_leg,
            neck,
            shoulders,
            waist,
            chest,
            hips,
            check_date: datetime):
        self.id = id
        self.pl_id = pl_id
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
            "pl_id": self.pl_id,
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
            "check_date": self.check_date.strftime("%Y/%m/%d, %H:%M:%S"),
        }

    @staticmethod
    def deserialize(json: dict):
        return Metric(
            json['id'],
            json['pl_id'],
            json['gym_id'],
            json['height'],
            json['weight'],
            json['l_arm'],
            json['r_arm'],
            json['l_humerus'],
            json['r_humerus'],
            json['l_thigh'],
            json['r_thigh'],
            json['l_leg'],
            json['r_leg'],
            json['neck'],
            json['shoulders'],
            json['waist'],
            json['chest'],
            json['hips'],
            datetime.strptime(json['check_date'], "%Y/%m/%d, %H:%M:%S"),
        )

