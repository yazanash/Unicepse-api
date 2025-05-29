import os

from flask import Blueprint, request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash

from src.Authentication.auth_service import token_required
from api.src.Authentication.profile_model import Profile
from src.Authentication.user_model import User
from src.common import status


profile_Bp = Blueprint('profile', __name__, url_prefix='/api/v1')


@profile_Bp.route("/profile", methods=["POST"])
@token_required
def create_profile(current_user):
    """this function will register a user"""
    try:
        data = request.get_json()
        exist_profile = Profile.find(current_user.uid)
        if exist_profile is not None:
            message = "This Profile is already exists"
            return make_response(jsonify(message), status.HTTP_409_CONFLICT)
        profile = Profile()
        profile.deserialize_by_token(data)
        profile.uid = current_user.uid
        profile.create()
        message = {'message': "profile Created Successfully", 'profile_info': profile.serialize()}
        return make_response(jsonify(message), status.HTTP_201_CREATED)
    except Exception as error:
        return make_response(jsonify(error), status.HTTP_500_INTERNAL_SERVER_ERROR)


@profile_Bp.route("/profile/<string:account_id>", methods=["GET"])
def get_profile(account_id):
    """this function will return user data"""
    profile = Profile.find(account_id)
    if profile is None:
        abort(status.HTTP_404_NOT_FOUND, f"Profile with id [{account_id}] could not be found.")
    message = profile.serialize()
    return make_response(jsonify(message), status.HTTP_200_OK)


@profile_Bp.route("/profile", methods=["GET"])
@token_required
def get_auth_profile(current_user):
    """this function will return user data"""
    profile = Profile.find(current_user.uid)
    if profile is None:
        abort(status.HTTP_404_NOT_FOUND, f"Profile with id [{current_user.uid}] could not be found.")
    message = profile.serialize()
    return make_response(jsonify(message), status.HTTP_200_OK)


@profile_Bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    """this function will UPDATE user data a"""
    if str(current_user.uid) == str(os.environ["GUEST_ID"]):
        abort(status.HTTP_403_FORBIDDEN, f"This profile is readonly")
    profile = Profile.find(current_user.uid)
    if profile is None:
        abort(status.HTTP_404_NOT_FOUND, f"Profile with id [{current_user.uid}] could not be found.")
    profile.deserialize_by_token(request.get_json())
    profile.update()
    message = {'message': 'profile updated successfully', 'user_info': profile.serialize()}
    return make_response(jsonify(message), status.HTTP_200_OK)


@profile_Bp.route("/profile/all", methods=["GET"])
def get_profiles_list():
    """this function will return all users """
    profiles = Profile.all()
    profile_list = [profile.serialize() for profile in profiles]
    return jsonify(profile_list), status.HTTP_200_OK



