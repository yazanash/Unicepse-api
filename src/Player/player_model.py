from src.Player.player_presistent_base import PlayerPersistentBase
from datetime import datetime
from src.common import status


class Player(PlayerPersistentBase):

    # dt_name = "players"
    # players_table = "players_table"

    def __init__(self, pid=None, name=None, width=None, height=None, date_of_birth=None, gender=None, balance=None):
        super().__init__()
        self.pid = pid
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
                json['pid'],
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
            'pid': self.pid,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'date_of_birth': self.date_of_birth.strftime("%Y/%m/%d, %H:%M:%S"),
            'gender': self.gender,
            'balance': self.balance,
        }

    @staticmethod
    def create_model():
        return Player()
