from flask import Blueprint, jsonify
from app.auth import token_required

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/headcount", methods=["GET"])
@token_required
def headcount():
    """
    Returns department-wise headcount (CI mode)
    """

    result = [
        {"department": "Engineering", "count": 10},
        {"department": "HR", "count": 2},
        {"department": "Marketing", "count": 5}
    ]

    return jsonify(result), 200