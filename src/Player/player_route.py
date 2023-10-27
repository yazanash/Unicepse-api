from flask import Blueprint, request, jsonify
from player_model import Player
from src.common import status
from player_service import  PlayerService


playerBp = Blueprint("player_info", __name__)
player_service = PlayerService()

"""
This module is responsible for handling Player route
it should be tied with a player service(controller)
"""


@playerBp.route("/player", methods=["POST"])
def create_player():
    """
    create player route...
    maybe this should be on the sign-in process?
    """
    try:
        player_service.create_player_usecase()
    except Exception :
        return status.HTTP_400_BAD_REQUEST
    return status.HTTP_503_SERVICE_UNAVAILABLE


@playerBp.route("/player", methods=["GET"])
def read_player():
    """
    get handler to retrieve player info
    a (Token) should be present to identify
    player and return info
    """
    return status.HTTP_503_SERVICE_UNAVAILABLE


@playerBp.route("/player", methods=["PUT"])
def update_player():
    """
    Update player info.
    info should be in json format
    """
    try:
        res = Player.deserialize(request.get_json())
    except Exception :
        return status.HTTP_400_BAD_REQUEST
    return res
