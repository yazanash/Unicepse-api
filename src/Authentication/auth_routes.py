from flask import Blueprint, request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash

from src.Authentication.auth_service import token_required
from src.Authentication.user_model import User
from src.common import status


auth_Bp = Blueprint('auth', __name__)


@auth_Bp.route("/auth", methods=["POST"])
def create_user():
    """this function will register a user"""
    try:
        # return make_response(jsonify("request called correctly"), status.HTTP_200_OK)
        data = request.get_json()
        exist_user = User.get_user_by_email(data["email"])
        if exist_user is not None:
            message = "This email is already exist"
            return make_response(jsonify(message), status.HTTP_409_CONFLICT)
        user = User()
        user.deserialize(data)
        user.create()

        User.send_email(user.email)
        message = {'message': "User Created Successfully", 'account_info': user.secret_serialize()}
        return make_response(jsonify(message), status.HTTP_201_CREATED)
    except Exception as error:
        return make_response(jsonify(error), status.HTTP_500_INTERNAL_SERVER_ERROR)


@auth_Bp.route("/auth/verify", methods=["POST"])
def verify_otp():
    """this function will register a user"""
    data = request.get_json()
    if User.verify_otp(data['email'], data['otp']):
        message = "verified successfully"
        user = User.get_user_by_email(data['email'])
        if user is not None:
            user.is_verified = True
            User.delete_from_otp((data['email']))
            print(user.serialize())
            user.update()
            print(user.serialize())
            return make_response(jsonify(message), status.HTTP_200_OK)
        message = "email is not exist"
        return make_response(jsonify(message), status.HTTP_404_NOT_FOUND)
    else:
        message = "verification Error otp is incorrect"
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
    user.deserialize_update(request.get_json())
    user.update()
    message = {'message': 'user updated successfully', 'user_info': user.secret_serialize()}
    return make_response(jsonify(message), status.HTTP_200_OK)


@auth_Bp.route("/auth", methods=["GET"])
def get_users_list():
    """this function will return all users """
    users = User.all()
    users_list = [user.secret_serialize() for user in users]
    return jsonify(users_list), status.HTTP_200_OK


@auth_Bp.route("/auth/login", methods=["POST"])
def login_user():
    """this function will log in user """
    credential = request.get_json()
    auth_user = User.get_user_by_email(credential['email'])
    token = auth_user.login_user(credential)
    if not token:
        abort(status.HTTP_401_UNAUTHORIZED, f"invalid Credential")
    return make_response(jsonify(token), status.HTTP_200_OK)


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


@auth_Bp.route("/auth/reset-password", methods=["POST"])
@token_required
def reset_new_password(current_user):
    """this function will register a user"""
    user = current_user
    print(user)
    if user is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{current_user.uid}] could not be found.")
    data = request.get_json()
    user.password = data['password']
    user.update_password()
    message = {'message': 'user updated successfully', 'user_info': user.secret_serialize()}
    return make_response(jsonify(message), status.HTTP_200_OK)
