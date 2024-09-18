from flask import Blueprint, request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash

from src.Authentication.auth_service import token_required
from src.Authentication.auth_validation import UserBaseSchema, UserSchema
from src.Authentication.user_model import User
from src.common import status

from marshmallow import ValidationError

auth_Bp = Blueprint('auth', __name__, url_prefix='/api/v1')


user_base_schema = UserBaseSchema()
user_schema = UserSchema()


@auth_Bp.route("/auth", methods=["POST"])
def create_user():
    """this function will register a user"""
    try:
        data = user_base_schema.load(request.json)
        User.send_email(data["email"])
        message = {'message': "Otp sent successfully"}
        return make_response(jsonify(message), status.HTTP_200_OK)
    # except Exception as error:
    #     return make_response(jsonify(error.), status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValidationError as err:
        return make_response(jsonify(err.messages), status.HTTP_400_BAD_REQUEST)


@auth_Bp.route("/auth/verify", methods=["POST"])
def verify_otp():
    """this function will register a user"""
    try:
        data = user_schema.load(request.json)

        if User.verify_otp(data['email'], data['otp']):
            message = "verified successfully"
            exist_user = User.get_user_by_email(data["email"])
            if exist_user is None:
                user = User()
                user.deserialize(data)
                user.create()
                token = user.generate_token()
                user.update()
                User.delete_from_otp((data['email']))
                return make_response(jsonify({"message": message, "token": token}), status.HTTP_201_CREATED)
            elif exist_user is not None:
                token = exist_user.generate_token()
                exist_user.update()
                User.delete_from_otp((data['email']))
                return make_response(jsonify({"message": message, "token": token}), status.HTTP_200_OK)
        else:
            message = "verification Error otp is incorrect"
            return make_response(jsonify(message), status.HTTP_401_UNAUTHORIZED)
    except ValidationError as err:
        return make_response(jsonify(err.messages), status.HTTP_400_BAD_REQUEST)

# @auth_Bp.route("/auth/<string:account_id>", methods=["GET"])
# def get_user(account_id):
#     """this function will return user data"""
#     user = User.find(account_id)
#     if user is None:
#         abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
#     message = user.serialize()
#     return make_response(jsonify(message), status.HTTP_200_OK)


@auth_Bp.route("/auth/<string:account_id>", methods=["PUT"])
def update_user(account_id):
    """this function will UPDATE user data a"""
    try:
        user = User.find(account_id)
        if user is None:
            abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
        user.deserialize_update(request.get_json())
        user.update()
        message = {'message': 'user updated successfully', 'user_info': user.secret_serialize()}
        return make_response(jsonify(message), status.HTTP_200_OK)
    except ValidationError as err:
        return make_response(jsonify(err.messages), status.HTTP_400_BAD_REQUEST)


@auth_Bp.route("/auth/refresh", methods=["PUT"])
@token_required
def update_token_user(current_user):
    """this function will UPDATE user data a"""
    try:
        user = User.find(current_user.uid)
        data = request.get_json()
        user.notify_token = data["notify_token"]
        token = user.generate_token()
        user.update()
        message = "updated successfully"
        return make_response(jsonify({"message": message, "token": token}), status.HTTP_201_CREATED)
    except ValidationError as err:
        return make_response(jsonify(err.messages), status.HTTP_400_BAD_REQUEST)


@auth_Bp.route("/auth", methods=["GET"])
def get_users_list():
    """this function will return all users """
    users = User.all()
    users_list = [user.secret_serialize() for user in users]
    return jsonify(users_list), status.HTTP_200_OK


@auth_Bp.route("/auth/logout", methods=["GET"])
@token_required
def logout_user(current_user):
    """this function will return all users """
    user = User.find(current_user.uid)
    user.token = None
    user.notify_token = None
    user.update()
    return jsonify({"logged out successfully"}), status.HTTP_200_OK

# @auth_Bp.route("/auth/login", methods=["POST"])
# def login_user():
#     """this function will log in user """
#     credential = request.get_json()
#     auth_user = User.get_user_by_email(credential['email'])
#     token = auth_user.login_user(credential)
#     if not token:
#         abort(status.HTTP_401_UNAUTHORIZED, f"invalid Credential")
#     return make_response(jsonify(token), status.HTTP_200_OK)


# @auth_Bp.route("/auth/reset", methods=["POST"])
# def reset_password():
#     """this function will log in user """
#     credential = request.get_json()
#     auth_user = User.get_user_by_email(credential['email'])
#     if auth_user is not None:
#         User.send_email(auth_user.email)
#         message = "otp sending successfully"
#         return make_response(jsonify(message), status.HTTP_200_OK)
#     else:
#         abort(status.HTTP_401_UNAUTHORIZED, f"invalid Credential")


# @auth_Bp.route("/auth/reset-password/verify", methods=["POST"])
# def verify_otp_for_password():
#     """this function will register a user"""
#     data = request.get_json()
#     if User.verify_otp(data['email'], data['otp']):
#         user = User.get_user_by_email(data['email'])
#         message = user.generate_token()
#         user.update()
#         return make_response(jsonify(message), status.HTTP_200_OK)
#     else:
#         message = "verified Error otp is incorrect"
#         return make_response(jsonify(message), status.HTTP_401_UNAUTHORIZED)


# @auth_Bp.route("/auth/reset-password", methods=["POST"])
# @token_required
# def reset_new_password(current_user):
#     """this function will register a user"""
#     user = current_user
#     print(user)
#     if user is None:
#         abort(status.HTTP_404_NOT_FOUND, f"Account with id [{current_user.uid}] could not be found.")
#     data = request.get_json()
#     user.password = data['password']
#     user.update_password()
#     message = {'message': 'user updated successfully', 'user_info': user.secret_serialize()}
#     return make_response(jsonify(message), status.HTTP_200_OK)
