from datetime import datetime
from src.payment import payment_persistent_base


class Payment(payment_persistent_base.PaymentPersistentBase):
    def __init__(self, id, pid, sid, gym_id, value, description, date: datetime):
        self.id = id
        self.pid = pid
        self.sid = sid
        self.gym_id = gym_id
        self.value = value
        self.description = description
        self.date = date

    def serialize(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'sid': self.sid,
            'gym_id': self.gym_id,
            'value': self.value,
            'description': self.description,
            'date': self.date.strftime("%d/%m/%Y")
        }

    @staticmethod
    def deserialize(json):
        return Payment(
            json["id"],
            json['value'],
            json['description'],
            datetime.strptime(json['date'], "%d/%m/%Y"),
        )
