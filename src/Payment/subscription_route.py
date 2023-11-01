from flask import Blueprint, request
from .subscription_service import SubscriptionService

subscriptionBp = Blueprint("Subscription", __name__)
route = "/subscription"
service = SubscriptionService()


@subscriptionBp.route(route, methods=["GET"])
def read_all_transactions():
    return service.read_subscription_usecase(request.get_json()['0'])


@subscriptionBp.route(route, methods=["POST"])
def create_transaction():
    return service.create_subscription_usecase(request.get_json())


@subscriptionBp.route(route, method=["PUT"])
def update_transaction():
    pass


@subscriptionBp.route(route, method=["DELETE"])
def delete_transaction():
    pass
