from flask import Blueprint, request

from src.api_key_protection import api_key_required
from src.plans.plan_services import PlanService

plans_bp = Blueprint("Plans", __name__, url_prefix='/api/v1')
route = "/plans"
service = PlanService()


@plans_bp.route(f"{route}/<id>", methods=["GET"])
@api_key_required
def read_plan(id):
    return service.read_plan_use_case(id)


@plans_bp.route(f"{route}", methods=["GET"])
@api_key_required
def read_plans():
    return service.read_plans_use_case()


@plans_bp.route(route, methods=["POST"])
@api_key_required
def create_plan():
    return service.create_plan_use_case(request.get_json())


@plans_bp.route(f"{route}/<id>", methods=["PUT"])
@api_key_required
def update_plan(id):
    return service.update_plan_use_case(request.get_json(),id)

