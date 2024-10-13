from flask import Blueprint, request

from src.api_key_protection import api_key_required
from src.license.license_service import LicenseService
from src.license.license_middleware import token_verification
licenses_bp = Blueprint("License", __name__, url_prefix='/api/v1')
route = "/licenses"
service = LicenseService()


@licenses_bp.route(f"{route}/get/<lid>", methods=["GET"])
def read_license(lid):
    return service.read_license_use_case(lid)


@licenses_bp.route(f"{route}/verify", methods=["GET"])
@token_verification
def verify_license(current_license):
    return service.verify_license_use_case(current_license)


@licenses_bp.route(f"{route}/<product_key>", methods=["GET"])
def read_license_by_product_key(product_key):
    return service.read_license_by_product_key_use_case(product_key)


@licenses_bp.route(f"{route}/gym/<gym_id>", methods=["GET"])
@api_key_required
def read_gym_licenses(gym_id):
    return service.read_gym_licenses_use_case(gym_id)


@licenses_bp.route(f"{route}", methods=["GET"])
@api_key_required
def read_licenses():
    return service.read_licenses_use_case()


@licenses_bp.route(route, methods=["POST"])
@api_key_required
def create_license():
    return service.create_license_use_case(request.get_json())


@licenses_bp.route(f"{route}/<lid>", methods=["PUT"])
@api_key_required
def update_license(lid):
    return service.update_license_use_case(request.get_json(), lid)
