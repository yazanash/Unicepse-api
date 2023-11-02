from flask import Blueprint, request
from payment_service import PaymentService

subscriptionBp = Blueprint("Payments", __name__)
route = "/payments"
service = PaymentService()


@subscriptionBp.route(route, methods=["GET"])
def read_all_transactions():
    return service.read_payment_use_case(request.get_json())


@subscriptionBp.route(route, methods=["POST"])
def create_transaction():
    return service.create_payment_use_case(request.get_json())


@subscriptionBp.route(route, method=["PUT"])
def update_transaction():
    return service.update_payment_use_case(request.get_json())


@subscriptionBp.route(route, method=["DELETE"])
def delete_transaction():
    return service.delete_payment_use_case(request.get_json())
