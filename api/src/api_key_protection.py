import os

from flask import request, jsonify
from functools import wraps


def api_key_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        print(api_key)
        print(os.environ['API_KEY'])
        if api_key != os.environ['API_KEY']:
            return jsonify({'message': 'Invalid API key!'}), 403
        return f(*args, **kwargs)

    return decorator
