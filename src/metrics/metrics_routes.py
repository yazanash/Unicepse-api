from flask import Blueprint, request
from metrics_service import MetricsService

subscriptionBp = Blueprint("Metrics", __name__)
route = "/metrics"
service = MetricsService()


@subscriptionBp.route(route, methods=["GET"])
def read_all_transactions():
    return service.read_metrics_usecase(request.get_json())


@subscriptionBp.route(route, methods=["POST"])
def create_transaction():
    return service.create_metric_usecase(request.get_json())


@subscriptionBp.route(route, method=["PUT"])
def update_transaction():
    return service.update_metric_usecase(request.get_json())


@subscriptionBp.route(route, method=["DELETE"])
def delete_transaction():
    return service.delete_metric_usecase(request.get_json())
