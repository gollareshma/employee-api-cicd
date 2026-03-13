import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

# Simple user store (normally this would be a database)
USERS = {
    "admin": {"password": "Admin@1234", "role": "admin"},
    "hr": {"password": "Hr@1234", "role": "hr"},
    "viewer": {"password": "View@1234", "role": "viewer"}
}

def generate_token(username, role):
    """Generate JWT token"""
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm="HS256"
    )

    return token


def token_required(f):
    """Protect routes with authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        token = token.replace("Bearer ", "")

        try:
            data = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"]
            )

            request.user = data

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """Only admin users allowed"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):

        if request.user.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return f(*args, **kwargs)

    return decorated