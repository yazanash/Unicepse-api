from datetime import datetime
from src.payment import payment_persistent_base


class Payment(payment_persistent_base.PaymentPersistentBase):
    def __init__(self,
                 id=None,
                 pid=None,
                 sid=None,
                 gym_id=None,
                 value=None,
                 description=None,
                 date=None):
        self.id = id
        self.pid = pid
        self.sid = sid
        self.gym_id = gym_id
        self.value = value
        self.description = description
        self.date = date

    def serialize(self):
        """should return json map for this model"""

        return {
            'id': self.id,
            'pid': self.pid,
            'sid': self.sid,
            'gym_id': self.gym_id,
            'value': self.value,
            'description': self.description,
            'date': self.date
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.id = json["id"]
        self.pid = json["pid"]
        self.sid = json["sid"]
        self.gym_id = json["gym_id"]
        self.value = json['value']
        self.description = json['description']
        self.date = json['date']

    @staticmethod
    def create_model():
        return Payment()
