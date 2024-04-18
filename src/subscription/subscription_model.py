from datetime import datetime
from .subscription_persistent_base import SubscriptionPersistentBase
from ..payment.payment_model import Payment


class Subscription(SubscriptionPersistentBase):

    def __init__(
            self,
            id,
            pl_id,
            gym_id,
            sport_name,
            trainer_name,
            start_date: datetime,
            end_date: datetime,
            price,
            discount_value,
            discount_des,
            is_payed,
            list_of_payments,
    ):
        self.id = id
        self.pl_id = pl_id
        self.gym_id = gym_id
        self.sport_name = sport_name
        self.trainer_name = trainer_name
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.discount_value = discount_value
        self.discount_des = discount_des
        self.is_payed = is_payed
        self.list_of_payments = list_of_payments

    @classmethod
    def deserialize(cls, json: dict):
        """should return json map for this model"""

        pays = json['list_of_payments']
        data = []
        if pays is not None:

            for p in pays:
                data.append(Payment.deserialize(p))

        return Subscription(
            id=json['id'],
            pl_id=json['pl_id'],
            gym_id=json["gym_id"],
            sport_name=json['sport_name'],
            trainer_name=json['trainer_name'],
            start_date=datetime.strptime(json['start_date'], "%Y/%m/%d, %H:%M:%S"),
            end_date=datetime.strptime(json['end_date'], "%Y/%m/%d, %H:%M:%S"),
            price=json['price'],
            discount_value=json['discount_value'],
            discount_des=json['discount_des'],
            is_payed=json['is_payed'],
            list_of_payments=data,
        )

    def serialize(self):
        data = []
        if self.list_of_payments is not None:

            for p in self.list_of_payments:
                data.append(p.serialize())

        return {
            'id': self.id,
            'pl_id': self.pl_id,
            'sp_id': self.sport_name,
            'tr_id': self.trainer_name,
            'start_date': self.start_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'end_date': self.end_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'price': self.price,
            'discount_value': self.discount_value,
            'discount_des': self.discount_des,
            'is_pay': self.is_payed,
            'list_of_payments': data,
        }
