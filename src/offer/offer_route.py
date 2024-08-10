from flask import Blueprint, request

from src.offer.offer_service import OfferService
from src.plans.plan_services import PlanService

offers_bp = Blueprint("Offers", __name__, url_prefix='/api/v1')
route = "/offers"
service = OfferService()


@offers_bp.route(f"{route}/<id>", methods=["GET"])
def read_offer(id):
    return service.read_offer_use_case(id)


@offers_bp.route(f"{route}", methods=["GET"])
def read_offers():
    return service.read_offers_use_case()


@offers_bp.route(route, methods=["POST"])
def create_offer():
    return service.create_offer_use_case(request.get_json())


@offers_bp.route(f"{route}/<id>", methods=["PUT"])
def update_offer(id):
    return service.update_offer_use_case(request.get_json(), id)

