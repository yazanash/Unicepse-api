from datetime import datetime
from .subscription_persistent_base import SubscriptionPersistentBase


class Subscription(SubscriptionPersistentBase):

    dt_name = "Subscriptions"

    def __init__(
            self,
            id,
            pl_id,
            sp_id,
            tr_id,
            start_date: datetime,
            end_date: datetime,
            price,
            price_ad,
            discount_value,
            discount_des,
            is_discount,
            is_pay,
            payment_total,
    ):
        self.id = id
        self.pl_id = pl_id
        self.sp_id = sp_id
        self.tr_id = tr_id
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.price_ad = price_ad
        self.discount_value = discount_value
        self.discount_des = discount_des
        self.is_discount = is_discount
        self.is_pay = is_pay
        self.payment_total = payment_total

    @classmethod
    def deserialize(cls, json: dict):
        """should return json map for this model"""
        return Subscription(
            json['id'],
            json['pl_id'],
            json['sp_id'],
            json['tr_id'],
            datetime.strptime(json['start_date'], "%Y/%m/%d, %H:%M:%S"),
            datetime.strptime(json['end_date'], "%Y/%m/%d, %H:%M:%S"),
            json['price'],
            json['price_ad'],
            json['discount_value'],
            json['discount_des'],
            json['is_discount'],
            json['is_pay'],
            json['payment_total'],
        )

    def serialize(self):
        return {
            'id': self.id,
            'pl_id': self.pl_id,
            'sp_id': self.sp_id,
            'tr_id': self.tr_id,
            'start_date': self.start_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'end_date': self.end_date.strftime("%Y/%m/%d, %H:%M:%S"),
            'price': self.price,
            'price_ad': self.price_ad,
            'discount_value': self.discount_value,
            'discount_des': self.discount_des,
            'is_discount': self.is_discount,
            'is_pay': self.is_pay,
            'payment_total': self.payment_total,
        }
