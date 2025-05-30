from flask import Blueprint, request, send_from_directory

from src.license.license_middleware import token_verification
from src.routine.routine_services import RoutineService

# from gridfs import GridFS
# from db import db

routineBlueprint = Blueprint("Routine", __name__, url_prefix='/api/v1')
route = "/routines"
service = RoutineService()


@routineBlueprint.route(f"{route}/<gym_id>/<pid>", methods=["GET"])
def read_routine(gym_id, pid):
    return service.read_routine_use_case(gym_id, pid)


@routineBlueprint.route(f"{route}/images/<int:group_id>/<file_name>")
def get_image(group_id, file_name):
    return send_from_directory(f'assets/{group_id}', file_name)


@routineBlueprint.route(route, methods=["POST"])
@token_verification
def create_routine(current_license):
    return service.create_routine_use_case(request.get_json())


@routineBlueprint.route(route, methods=["PUT"])
@token_verification
def update_transaction(current_license):
    return service.update_routine_use_case(request.get_json())

