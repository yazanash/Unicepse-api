from flask import Blueprint, request

from src.attedence.attendance_services import AttendanceService
from src.license.license_middleware import token_verification

attendances_bp = Blueprint("Attendances", __name__, url_prefix='/api/v1')
route = "/attendances"
service = AttendanceService()


@attendances_bp.route(f"{route}/<gym_id>/<pid>", methods=["GET"])
def read_attendances(gym_id, pid):
    return service.read_attendances_use_case(pid, gym_id)


@attendances_bp.route(route, methods=["POST"])
@token_verification
def create_attendance(current_license):
    return service.create_attendance_use_case(request.get_json())


@attendances_bp.route(route, methods=["PUT"])
@token_verification
def update_attendance(current_license):
    return service.update_attendance_use_case(request.get_json())

