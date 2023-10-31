from flask import Blueprint, request
from .subscription_service import SubscriptionService

subscriptionBp = Blueprint("Subscription", __name__)
route = "/subscription"


@subscriptionBp.route(route, methods=["GET"])
def get_transaction():
    pass


@subscriptionBp.route(route, methods=["POST"])
def create_transaction():
    pass


@subscriptionBp.route(route, method=["PUT"])
def update_transaction():
    pass


@subscriptionBp.route(route, method=["DELETE"])
def delete_transaction():
    pass
