from src.Player.player_presistent_base import PlayerPersistentBase
from datetime import datetime
from src.common import status, errors
from src.common.utils import logger


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
            logger.info(f"deserializing a player")
            player = Player(
                json['pid'],
                json['name'],
                json['width'],
                json['height'],
                datetime.strptime(json['date_of_birth'], "%Y/%m/%d, %H:%M:%S"),
                json['gender'],
                json['balance'],
            )
        except AttributeError as e:
            logger.error("Error deserializing player: %s", e)
            raise errors.DataValidationError("Player deserializing Error!")
        except TypeError:
            raise errors.DataValidationError("TypeError")
        return player

    def serialize(self):
        """Serializes player to dict {json}"""
        try:

            mapping = {
                'pid': self.pid,
                'name': self.name,
                'width': self.width,
                'height': self.height,
                'date_of_birth': self.date_of_birth.strftime("%Y/%m/%d, %H:%M:%S"),
                'gender': self.gender,
                'balance': self.balance,
            }
            return mapping
        except AttributeError as e:
            logger.error("Error in serializing player: %s", e.args[0])
            raise errors.DataValidationError("DataValidationError in serialize player!!")

    @staticmethod
    def create_model():
        return Player()
