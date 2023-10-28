from player_model import Player
from src.common import status
import logging

logger = logging.getLogger("flask.app")


class PlayerService:
    """Player service class represents Use-cases of player model"""

    def create_player_usecase(self, player_json):
        try:
            player = Player.deserialize(player_json)
            if not Player.check_if_exist(player.id):
                player.create()
                return status.HTTP_201_CREATED
        except Exception as err:
            logger.error(f"Error Creating Player!! maybe data corrupted? {err.args[0]}")
            return status.HTTP_406_NOT_ACCEPTABLE

    def read_player_usecase(self, by_id):
        try:
            player = Player.find(by_id)
            if not player:
                return player
            return status.HTTP_204_NO_CONTENT
        except Exception as err:
            logger.error(f"Error could not process read player!! {err.args[0]}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_player_usecase(self, player):
        try:
            player.update()
            return status.HTTP_200_OK
        except Exception as err:
            logger.error(f"could not process update player!! {err.args[0]}")
            return status.HTTP_406_NOT_ACCEPTABLE

    def delete_player_usecase(self, by_id):
        try:
            player = Player.find(by_id)
            if not player:
                player.delete()
                return status.HTTP_200_OK
            return status.HTTP_406_NOT_ACCEPTABLE
        except Exception as err:
            logger.error(f"Error could not process Delete player!! {err.args[0]}")
