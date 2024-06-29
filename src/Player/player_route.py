from flask import Blueprint, request, make_response, jsonify
from src.Player.player_service import PlayerService
from src.common import status

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
    status_code = player_service.create_player_usecase(request.get_json())
    response = make_response()
    response.status_code = status_code
    return response


@playerBp.route("/player", methods=["GET"])
def read_player():
    """
    get handler to retrieve player info
    a (Token) should be present to identify
    player and return info
    """
    data = request.get_json()
    try:
        if 'gym_id' in data and 'pid' in data:
            player = player_service.read_player_usecase(data["gym_id"], data["pid"])
            if type(player) is int:
                return {}, player
            return make_response(player.serialize(), status.HTTP_200_OK)
        else:
            return make_response(jsonify({"Bad request": "required data is missing "}), status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return make_response(jsonify({"Bad request": error}), status.HTTP_400_BAD_REQUEST)


@playerBp.route("/player", methods=["PUT"])
def update_player():
    """
    Update player info.
    info should be in json format
    """
    print("update methode request json: ", request.get_json())
    stat = player_service.update_player_usecase(request.get_json())
    return make_response("Updated Successfully!", stat)
