import os

from flask import request, jsonify
from flask import current_app
import jwt
from functools import wraps
from src.Authentication.user_model import User
from src.common import status


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !! Failed to authorizing '}), status.HTTP_401_UNAUTHORIZED
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=["HS256"])
            print(data)
            current_user = User.find(data['public_id'])
            print(current_user.secret_serialize())
        except TypeError:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged-in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated
