from flask import Blueprint, request
from src.metrics.metrics_service import MetricsService

metrics_bp = Blueprint("Metrics", __name__)
route = "/metrics"
service = MetricsService()


@metrics_bp.route(f"{route}/<int:gym_id>/<int:pid>", methods=["GET"])
def read_all_metrics(gym_id, pid):
    return service.read_metrics_use_case(gym_id, pid)


@metrics_bp.route(f"{route}/<int:gym_id>/<int:pid>/<int:id>", methods=["GET"])
def read_single_metrics(gym_id, pid, id):
    return service.read_single_metrics_use_case(gym_id, pid, id)


@metrics_bp.route(route, methods=["POST"])
def create_metrics():
    return service.create_metric_use_case(request.get_json())


@metrics_bp.route(route, methods=["PUT"])
def update_metrics():
    return service.update_metric_use_case(request.get_json())

