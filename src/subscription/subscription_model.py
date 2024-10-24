from datetime import datetime
from .subscription_persistent_base import SubscriptionPersistentBase
from ..payment.payment_model import Payment


class Subscription(SubscriptionPersistentBase):

    def __init__(
            self,
            id=None,
            pid=None,
            gym_id=None,
            sport_name=None,
            trainer_name=None,
            start_date=None,
            end_date=None,
            price=None,
            discount_value=None,
            discount_des=None,
            is_paid=None,
            paid_value=None,
            payments=None,
    ):
        self.id = id
        self.pid = pid
        self.gym_id = gym_id
        self.sport_name = sport_name
        self.trainer_name = trainer_name
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.discount_value = discount_value
        self.discount_des = discount_des
        self.is_paid = is_paid
        self.paid_value = paid_value
        self.payments = payments

    def deserialize(self, json: dict):
        """should return this model from dict"""
        self.id = json['id']
        self.pid = json['pid']
        self.gym_id = json["gym_id"]
        self.sport_name = json['sport_name']
        self.trainer_name = json['trainer_name']
        self.start_date =json['start_date']
        self.end_date = json['end_date']
        self.price = json['price']
        self.discount_value = json['discount_value']
        self.discount_des = json['discount_des']
        self.is_paid = json['is_paid']
        self.paid_value = json['paid_value']

    def serialize(self):
        """should return json map for this model"""
        data = {}
        if self.payments is not None:

            for p in self.payments:
                data[p.id] = (p.serialize())

        return {
            'id': self.id,
            'pid': self.pid,
            'gym_id': self.gym_id,
            'sport_name': self.sport_name,
            'trainer_name': self.trainer_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'price': self.price,
            'discount_value': self.discount_value,
            'discount_des': self.discount_des,
            'is_paid': self.is_paid,
            'paid_value': self.paid_value,
        }

    @staticmethod
    def create_model():
        return Subscription()
