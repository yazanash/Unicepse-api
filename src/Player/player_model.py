from src.Player.player_presistent_base import PlayerPersistentBase
from datetime import datetime
from src.common import status, errors
from src.common.utils import logger


class Player(PlayerPersistentBase):

    def __init__(self, pid=None, name=None, phone_num=None, width=None, height=None,
                 date_of_birth=None, gender=None, balance=None, gym_id=None):
        super().__init__()
        self.pid = pid
        self.name = name
        self.phone_num = phone_num
        self.width = width
        self.height = height
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.balance = balance
        self.gym_id = gym_id

    def deserialize(self, json):
        """Deserializes a player from dict {json}"""
        try:
            logger.info(f"deserializing a player")
            self.pid = json["pid"]
            print(json)
            self.pid = json.get("pid")                      # NULLABLE
            self.name = json['name']
            self.phone_num = json['phone_num']
            self.width = json.get('width')                  # NULLABLE
            self.height = json.get('height')                # NULLABLE
            self.date_of_birth = json['date_of_birth']
            self.gender = json['gender']
            self.balance = json.get('balance')              # NULLABLE
            self.gym_id = json.get("gym_id")                # NULLABLE
        except AttributeError as e:
            logger.error("Error deserializing player: %s", e)
            raise errors.DataValidationError("Player deserializing Error!")
        except TypeError:
            raise errors.DataValidationError("TypeError")

    def serialize(self):
        """Serializes player to dict {json}"""
        try:

            mapping = {
                'pid': self.pid,
                'gym_id': self.gym_id,
                'phone_num': self.phone_num,
                'name': self.name,
                'width': self.width,
                'height': self.height,
                'date_of_birth': self.date_of_birth,
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
