from datetime import datetime


class Payment:
    def __init__(self, id, value, description, date: datetime):
        self.id = id
        self.value = value
        self.description = description
        self.date = date

    def serialize(self):
        return {
            'id': self.id,
            'value': self.value,
            'description': self.description,
            'date': self.date.strftime("%Y/%m/%d, %H:%M:%S")
        }

    @staticmethod
    def deserialize(json):
        return Payment(
            json['id'],
            json['value'],
            json['description'],
            datetime.strptime(json['date'], "%Y/%m/%d, %H:%M:%S"),
        )
