from flask import Blueprint, request, make_response
from .subscription_service import SubscriptionService
from ..license.license_middleware import token_verification

subscriptionBp = Blueprint("Subscription", __name__, url_prefix='/api/v1')
route = "/subscription"
service = SubscriptionService()


@subscriptionBp.route(f"{route}/<gym_id>/<pid>", methods=["GET"])
def read_all_transactions(gym_id, pid):
    return service.read_subscription_use_case(gym_id, pid)


@subscriptionBp.route(f"{route}/<gym_id>/<pid>/<id>", methods=["GET"])
def read_single_transactions(gym_id, pid, id):
    return service.read_single_subscription_use_case(gym_id, pid,id)


@subscriptionBp.route(route, methods=["POST"])
@token_verification
def create_transaction(current_license):
    return service.create_subscription_use_case(request.get_json())


@subscriptionBp.route(route, methods=["PUT"])
@token_verification
def update_transaction(current_license):
    return service.update_subscription_use_case(request.get_json())

