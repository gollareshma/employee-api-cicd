import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

USERS = {
    "admin": {"password": "Admin@1234", "role": "admin"}
}


def generate_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
            request.user = data
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated