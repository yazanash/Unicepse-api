from flask import Blueprint, request, make_response
from .subscription_service import SubscriptionService

subscriptionBp = Blueprint("Subscription", __name__, url_prefix='/api/v1')
route = "/subscription"
service = SubscriptionService()


@subscriptionBp.route(f"{route}/<int:gym_id>/<int:pid>", methods=["GET"])
def read_all_transactions(gym_id, pid):
    return service.read_subscription_use_case(gym_id, pid)


@subscriptionBp.route(f"{route}/<int:gym_id>/<int:pid>/<int:id>", methods=["GET"])
def read_single_transactions(gym_id, pid, id):
    return service.read_single_subscription_use_case(gym_id, pid,id)


@subscriptionBp.route(route, methods=["POST"])
def create_transaction():
    print("create called")
    return service.create_subscription_use_case(request.get_json())


@subscriptionBp.route(route, methods=["PUT"])
def update_transaction():
    return service.update_subscription_use_case(request.get_json())

