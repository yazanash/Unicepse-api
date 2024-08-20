from flask import Blueprint, request, send_from_directory

from src.routine.routine_services import RoutineService

# from gridfs import GridFS
# from db import db

routineBlueprint = Blueprint("Routine", __name__, url_prefix='/api/v1')
route = "/routines"
service = RoutineService()


@routineBlueprint.route(f"{route}/<int:gym_id>/<int:pid>", methods=["GET"])
def read_routine(gym_id, pid):
    return service.read_routine_use_case(gym_id, pid)


@routineBlueprint.route(f"{route}/images/<int:group_id>/<file_name>")
def get_image(group_id, file_name):
    print(f"image got {group_id} / {file_name} ")
    return send_from_directory(f'assets/{group_id}', file_name)


@routineBlueprint.route(route, methods=["POST"])
def create_routine():
    return service.create_routine_use_case(request.get_json())


@routineBlueprint.route(route, methods=["PUT"])
def update_transaction():
    return service.update_routine_use_case(request.get_json())

