from flask import Blueprint, jsonify
from app.auth import token_required

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/headcount", methods=["GET"])
@token_required
def headcount():

    data = {
        "Engineering": 10,
        "Marketing": 5,
        "HR": 2
    }

    return jsonify(data), 200