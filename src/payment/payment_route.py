from flask import Blueprint, request

from src.license.license_middleware import token_verification
from src.payment.payment_service import PaymentService

payments_bp = Blueprint("Payments", __name__, url_prefix='/api/v1')
route = "/payments"
service = PaymentService()


@payments_bp.route(f"{route}/<gym_id>/<pid>/<sid>", methods=["GET"])
def read_payments(gym_id, pid, sid):
    return service.read_payments_use_case(gym_id, pid, sid)
    # return service.read_payment_use_case({"gym_id": gym_id, "pl_id": pl_id, "sub_id": sub_id})


@payments_bp.route(f"{route}/<gym_id>/<pid>/<sid>/<id>", methods=["GET"])
def read_payment(gym_id, pid, sid, id):
    return service.read_payment_use_case(gym_id, pid, sid, id)


@payments_bp.route(route, methods=["POST"])
@token_verification
def create_transaction():
    return service.create_payment_use_case(request.get_json())


@payments_bp.route(route, methods=["PUT"])
@token_verification
def update_transaction():
    return service.update_payment_use_case(request.get_json())


@payments_bp.route(f"{route}/<int:gym_id>/<int:pid>/<int:sid>/<int:id>", methods=["DELETE"])
@token_verification
def delete_transaction(gym_id, pid, sid, id):
    return service.delete_payment_use_case(gym_id, pid, sid, id)
