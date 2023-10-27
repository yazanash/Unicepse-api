from src.common import models
from datetime import datetime
from src.common import status


class Player(models.PersistentBase):
    def __init__(self, id, name, width, height, date_of_birth: datetime, gender, balance):
        super().__init__()
        self.id = id
        self.name = name
        self.width = width
        self. height = height
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.balance = balance

    @staticmethod
    def deserialize(json):
        """Deserializes a player from dict {json}"""
        try:
            player = Player(
                json['id'],
                json['name'],
                json['width'],
                json['height'],
                datetime.strptime(json['date_of_birth'], "%Y/%m/%d, %H:%M:%S"),
                json['gender'],
                json['balance'],
            )
        except Exception:
            return status.HTTP_406_NOT_ACCEPTABLE
        return player

    def serialize(self):
        """Serializes player to dict {json}"""
        return {
            'id': self.id,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'date_of_birth': self.date_of_birth.strftime("%Y/%m/%d, %H:%M:%S"),
            'gender': self.gender,
            'balance': self.balance,
        }
