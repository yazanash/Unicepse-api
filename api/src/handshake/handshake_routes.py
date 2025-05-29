from flask import Blueprint, request

from src.api_key_protection import api_key_required
from src.handshake.handshake_service import HandShakeService
from src.handshake.hanshake_validation import HandShakeBaseSchema

handshakes_bp = Blueprint("HandShake", __name__, url_prefix='/api/v1')
route = "/handshake"
service = HandShakeService()


@handshakes_bp.route(f"{route}/<uid>", methods=["GET"])
def read_hand_shakes(uid):
    return service.read_hand_shakes_use_case(uid)


@handshakes_bp.route(route, methods=["POST"])
def create_hand_shakes():
    return service.create_hand_shack_use_case(request.get_json())


@handshakes_bp.route(f"{route}/<gym_id>/notify", methods=["POST"])
@api_key_required
def send_gym_players_notifications(gym_id):
    return service.send_gym_players_notifications_use_case(gym_id, request.get_json())


@handshakes_bp.route(f"{route}/notify", methods=["POST"])
@api_key_required
def send_all_players_notifications():
    return service.send_all_players_notifications_use_case(request.get_json())

