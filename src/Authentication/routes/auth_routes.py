import os

import jwt
from firebase_admin import auth
from flask import Blueprint, request, jsonify, make_response, abort
from src.Authentication.models.user_model import User
from src.common import status
# from tests.factories import UserFactory

auth_Bp = Blueprint('email_auth', __name__)


@auth_Bp.route("/auth", methods=["POST"])
def create_user():
    """this function will register a user"""
    user = User()
    user.deserialize(request.get_json())
    user.create()
    message = user.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)


@auth_Bp.route("/auth/<string:account_id>", methods=["GET"])
def get_user(account_id):
    """this function will return user data"""
    user = User.find(account_id)
    if user is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    message = user.serialize()
    return make_response(jsonify(message), status.HTTP_200_OK)


@auth_Bp.route("/auth/<string:account_id>", methods=["PUT"])
def update_user(account_id):
    """this function will UPDATE user data a"""
    user = User.find(account_id)
    if user is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    user.deserialize(request.get_json())
    user.update()
    message = user.serialize()
    return make_response(jsonify(message), status.HTTP_200_OK)


@auth_Bp.route("/auth", methods=["GET"])
def get_users_list():
    """this function will return all users """
    users = User.all()
    users_list = [user.serialize() for user in users]
    return jsonify(users_list), status.HTTP_200_OK


@auth_Bp.route("/auth/login", methods=["POST"])
def login_user():
    """this function will UPDATE user data a"""
    credential = request.get_json()
    auth_user = User.get_user_by_email(credential['email'])
    token = auth_user.login_user(credential)
    if not token:
        abort(status.HTTP_401_UNAUTHORIZED, f"invalid Credential")
    return make_response(jsonify(token), status.HTTP_200_OK)
