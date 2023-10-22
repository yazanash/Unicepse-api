from flask import Blueprint, request, jsonify
from src.Authentication.models.user_model import User
from src.common import status

authBp = Blueprint('email_auth', __name__)


@authBp.route("/register", methods=["POST"])
def register():
    try:
        user = User()
        user.deserialize(data=request.get_json())
        return status.HTTP_201_CREATED
    except Exception :  # noqa
        return status.HTTP_400_BAD_REQUEST


@authBp.route("/login", methods=["POST"])
def login():
    try:
        user = User()
        user.deserialize(request.get_json())
        return status.HTTP_201_CREATED
    except Exception :  # noqa
        return status.HTTP_400_BAD_REQUEST
