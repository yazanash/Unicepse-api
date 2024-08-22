from flask import Blueprint, request

from src.Authentication.auth_service import token_required
from src.gym.gym_service import GymService
from src.handshake.handshake_service import HandShakeService
from src.handshake.hanshake_validation import HandShakeBaseSchema

gyms_bp = Blueprint("Gyms", __name__, url_prefix='/api/v1')
route = "/gyms"
service = GymService()


@gyms_bp.route(f"{route}/<id>", methods=["GET"])
def read_gym(id):
    return service.read_gym_use_case(id)


@gyms_bp.route(f"{route}", methods=["GET"])
def read_gyms():
    return service.read_gyms_use_case()


@gyms_bp.route(f"{route}", methods=["GET"])
@token_required
def read_gyms(current_user):
    return service.read_user_gyms_use_case(current_user)


@gyms_bp.route(route, methods=["POST"])
def create_gym():
    return service.create_gym_use_case(request.get_json())


@gyms_bp.route(route, methods=["PUT"])
def update_gym():
    return service.update_gym_use_case(request.get_json())

