from flask import Blueprint, request
from src.license.license_service import LicenseService

licenses_bp = Blueprint("License", __name__, url_prefix='/api/v1')
route = "/licenses"
service = LicenseService()


@licenses_bp.route(f"{route}/get/<lid>", methods=["GET"])
def read_license(lid):
    return service.read_license_use_case(lid)


@licenses_bp.route(f"{route}/<product_key>", methods=["GET"])
def read_license_by_product_key(product_key):
    return service.read_license_by_product_key_use_case(product_key)


@licenses_bp.route(f"{route}/gym/<gym_id>", methods=["GET"])
def read_gym_licenses(gym_id):
    return service.read_gym_licenses_use_case(gym_id)


@licenses_bp.route(f"{route}", methods=["GET"])
def read_licenses():
    return service.read_licenses_use_case()


@licenses_bp.route(route, methods=["POST"])
def create_license():
    return service.create_license_use_case(request.get_json())


@licenses_bp.route(f"{route}/<lid>", methods=["PUT"])
def update_license(lid):
    return service.update_license_use_case(request.get_json(), lid)
