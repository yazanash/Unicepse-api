from flask import Blueprint, request
from src.payment.payment_service import PaymentService

payments_bp = Blueprint("Payments", __name__)
route = "/payments/<int:gym_id>/<int:pl_id>/<int:sub_id>/<int:id>"
route2 = "/payments/<int:gym_id>/<int:pl_id>/<int:sub_id>"
service = PaymentService()


@payments_bp.route(route2, methods=["GET"])
def read_all_transactions():
    return service.read_payment_use_case(request.get_json())
    # return service.read_payment_use_case({"gym_id": gym_id, "pl_id": pl_id, "sub_id": sub_id})


@payments_bp.route(route, methods=["POST"])
def create_transaction():
    return service.create_payment_use_case(request.get_json())


@payments_bp.route(route, methods=["PUT"])
def update_transaction():
    return service.update_payment_use_case(request.get_json())


@payments_bp.route(route, methods=["DELETE"])
def delete_transaction():
    return service.delete_payment_use_case(request.get_json())
