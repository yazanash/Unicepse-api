from flask import Blueprint, request

from src.handshake.handshake_service import HandShakeService
from src.handshake.hanshake_validation import HandShakeBaseSchema

handshakes_bp = Blueprint("HandShake", __name__, url_prefix='/api/v1')
route = "/handshake"
service = HandShakeService()


@handshakes_bp.route(f"{route}/<int:uid>", methods=["GET"])
def read_hand_shakes(uid):
    return service.read_hand_shakes_use_case(uid)


@handshakes_bp.route(route, methods=["POST"])
def create_hand_shakes():
    return service.create_hand_shack_use_case(request.get_json())

