from .player_model import Player
from src.common import status, errors
from src.common.utils import logger
from .player_validator import validate_player


class PlayerService:
    """Player service class represents Use-cases of player model"""

    def create_player_usecase(self, player_json):
        """create player service called from route to handle usecase"""
        try:
            logger.info("Try create player from json")
            validate_player(player_json)
            if not Player.check_if_exist(player_json['pid']):
                player = Player.deserialize(player_json)
                player.create()
                logger.info(f"Player {player.name} : {player.pid} created!!!")
                return status.HTTP_201_CREATED
            return status.HTTP_409_CONFLICT
        except errors.DataValidationError as err:
            logger.error(f"Error Creating Player!! maybe data corrupted? {err.args[0]}")
            return status.HTTP_406_NOT_ACCEPTABLE

    def read_player_usecase(self, by_id):
        """read player service called from route to handle usecase"""
        try:
            if Player.check_if_exist(by_id):
                player = Player.find(by_id)
                return player
            return status.HTTP_404_NOT_FOUND
        except Exception as err:
            logger.error(f"Error could not process read player!! {err.args[0]}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_player_usecase(self, player_json):
        """update player service called from route to handle usecase"""
        try:
            validate_player(player_json)
            player = Player.deserialize(player_json)
            player.update()
            return status.HTTP_200_OK
        except errors.DataValidationError as err:
            logger.error(f"could not process update player!! {err.args[0]}")
            return status.HTTP_406_NOT_ACCEPTABLE

    def delete_player_usecase(self, by_id):
        """delete player service called from route to handle usecase"""
        try:
            if Player.check_if_exist(by_id):
                player = Player.find(by_id)
                player.delete()
                return status.HTTP_200_OK
            return status.HTTP_404_NOT_FOUND
        except Exception as err:
            logger.error(f"Error could not process Delete player!! {err.args[0]}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR
