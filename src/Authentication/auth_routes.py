from flask import Blueprint, request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash

from src.Authentication.user_model import User
from src.common import status


auth_Bp = Blueprint('auth', __name__)


@auth_Bp.route("/auth", methods=["POST"])
def create_user():
    """this function will register a user"""
    # try:
    # return make_response(jsonify("request called correctly"), status.HTTP_200_OK)
    user = User()
    user.deserialize(request.get_json())
    user.create()

    User.send_email(user.email)
    message = user.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)
    # except Exception as error:
    #     return make_response(jsonify(error), status.HTTP_201_CREATED)


@auth_Bp.route("/auth/verify", methods=["POST"])
def verify_otp():
    """this function will register a user"""
    data = request.get_json()
    if User.verify_otp(data['email'], data['otp']):
        message = "verified successfully"
        user = User.get_user_by_email(data['email'])
        if user is not None:
            user.is_verified = True
            user.update()
            return make_response(jsonify(message), status.HTTP_200_OK)
        message = "email is not exist"
        return make_response(jsonify(message), status.HTTP_404_NOT_FOUND)
    else:
        message = "verified Error otp is incorrect"
        return make_response(jsonify(message), status.HTTP_401_UNAUTHORIZED)


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
    """this function will log in user """
    credential = request.get_json()
    auth_user = User.get_user_by_email(credential['email'])
    print(auth_user.serialize())
    token = auth_user.login_user(credential)
    return make_response(jsonify(token), status.HTTP_200_OK)
    # if not token:
    #     abort(status.HTTP_401_UNAUTHORIZED, f"invalid Credential")
    # return make_response(jsonify(token), status.HTTP_200_OK)


@auth_Bp.route("/auth/reset", methods=["POST"])
def reset_password():
    """this function will log in user """
    credential = request.get_json()
    auth_user = User.get_user_by_email(credential['email'])
    if auth_user is not None:
        User.send_email(auth_user.email)
        message = "otp sending successfully"
        return make_response(jsonify(message), status.HTTP_200_OK)
    else:
        abort(status.HTTP_401_UNAUTHORIZED, f"invalid Credential")


@auth_Bp.route("/auth/reset-password/verify", methods=["POST"])
def verify_otp_for_password():
    """this function will register a user"""
    data = request.get_json()
    if User.verify_otp(data['email'], data['otp']):
        user = User.get_user_by_email(data['email'])
        message = user.generate_token()
        user.update()
        return make_response(jsonify(message), status.HTTP_200_OK)
    else:
        message = "verified Error otp is incorrect"
        return make_response(jsonify(message), status.HTTP_401_UNAUTHORIZED)