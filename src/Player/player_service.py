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
            print("data validated")
            if Player.find(player_json['gym_id'], player_json['pid']) is None:
                player = Player.create_model()
                player.deserialize(player_json)
                player.create()
                print("data created")
                logger.info(f"Player {player.name} : {player.pid} created!!!")
                return status.HTTP_201_CREATED
            return status.HTTP_409_CONFLICT
        except errors.DataValidationError as err:
            logger.error(f"Error Creating Player!! maybe data corrupted? {err.args[0]}")
            return status.HTTP_406_NOT_ACCEPTABLE

    def read_player_usecase(self, gym_id, by_id):
        """read player service called from route to handle use case"""
        try:
            print(f"read player accessed {gym_id}, {by_id}")
            if Player.check_if_exist(gym_id, by_id):
                print("player is exists")
                player = Player.find(gym_id, by_id)
                return player
            return status.HTTP_404_NOT_FOUND
        except Exception as err:
            logger.error(f"Error could not process read player!! {err.args[0]}")
            return status.HTTP_400_BAD_REQUEST

    def update_player_usecase(self, player_json):
        """update player service called from route to handle use case"""
        try:
            validate_player(player_json)
            player = Player.create_model()
            player.deserialize(player_json)
            player.update()
            return status.HTTP_200_OK
        except errors.DataValidationError as err:
            logger.error(f"could not process update player!! {err.args[0]}")
            return status.HTTP_406_NOT_ACCEPTABLE

