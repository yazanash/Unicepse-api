from flask import Blueprint, request

from src.attedence.attendance_services import AttendanceService

attendances_bp = Blueprint("Attendances", __name__, url_prefix='/api/v1')
route = "/attendances"
service = AttendanceService()


@attendances_bp.route(f"{route}/<gym_id>/<pid>", methods=["GET"])
def read_attendances(gym_id, pid):
    return service.read_attendances_use_case(gym_id, pid)


@attendances_bp.route(route, methods=["POST"])
def create_attendance():
    return service.create_attendance_use_case(request.get_json())


@attendances_bp.route(route, methods=["PUT"])
def update_attendance():
    return service.update_attendance_use_case(request.get_json())

