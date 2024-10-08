from flask import Blueprint, request

from src.Authentication.auth_service import token_required
from src.license.license_middleware import token_verification
from src.metrics.metrics_service import MetricsService

metrics_bp = Blueprint("Metrics", __name__, url_prefix='/api/v1')
route = "/metrics"
service = MetricsService()


@metrics_bp.route(f"{route}", methods=["GET"])
@token_required
def read_all_metrics(current_user):
    return service.read_metrics_use_case(current_user)


@metrics_bp.route(f"{route}/<gym_id>/<pid>/<id>", methods=["GET"])
def read_single_metrics(gym_id, pid, id):
    return service.read_single_metrics_use_case(gym_id, pid, id)


@metrics_bp.route(route, methods=["POST"])
@token_verification
def create_metrics(current_license):
    return service.create_metric_use_case(request.get_json())


@metrics_bp.route(route, methods=["PUT"])
@token_verification
def update_metrics(current_license):
    return service.update_metric_use_case(request.get_json())

