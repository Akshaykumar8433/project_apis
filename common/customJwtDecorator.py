from flask import jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# decorator that verifies the JWT is present in the request and type is user
def admin_jwt_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            try:
                claims = get_jwt()
                if claims["role"] == 'admin':
                    return fn(*args, **kwargs)
                else:
                    return jsonify({ "status": 400, "message": "Request not allowed." })
            except Exception as e:
                return jsonify({"status":1500,"message":"Wrong access token"})
        return decorator
    return wrapper