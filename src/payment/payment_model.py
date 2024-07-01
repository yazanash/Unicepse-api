from datetime import datetime
from src.payment import payment_persistent_base


class Payment(payment_persistent_base.PaymentPersistentBase):
    def __init__(self, id, pl_id, sub_id, gym_id, value, description, date: datetime):
        self.id = id
        self.pl_id = pl_id
        self.sub_id = sub_id
        self.gym_id = gym_id
        self.value = value
        self.description = description
        self.date = date

    def serialize(self):
        return {
            'id': self.id,
            'pl_id': self.pl_id,
            'sub_id': self.sub_id,
            'gym_id': self.gym_id,
            'value': self.value,
            'description': self.description,
            'date': self.date.strftime("%Y/%m/%d, %H:%M:%S")
        }

    @staticmethod
    def deserialize(json):
        return Payment(
            json["id"],
            json['value'],
            json['description'],
            datetime.strptime(json['date'], "%Y/%m/%d, %H:%M:%S"),
        )
