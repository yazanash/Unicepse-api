from flask import Blueprint, request
from src.metrics.metrics_service import MetricsService

metrics_bp = Blueprint("Metrics", __name__, subdomain="api")
route = "/metrics"
service = MetricsService()


@metrics_bp.route(route, methods=["GET"])
def read_all_transactions():
    return "<h1>Metrics Route, WELCOME</h1>"
    # return service.read_metrics_usecase(request.get_json())


@metrics_bp.route(route, methods=["POST"])
def create_transaction():
    return service.create_metric_usecase(request.get_json())


@metrics_bp.route(route, methods=["PUT"])
def update_transaction():
    return service.update_metric_usecase(request.get_json())


@metrics_bp.route(route, methods=["DELETE"])
def delete_transaction():
    return service.delete_metric_usecase(request.get_json())
