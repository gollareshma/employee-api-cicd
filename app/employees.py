from flask import Blueprint, jsonify
from app.auth import token_required

employees_bp = Blueprint("employees", __name__)


@employees_bp.route("/", methods=["GET"])
@token_required
def get_all_employees():

    # CI mode (no DB)
    employees = [
        {"id": 1, "name": "John", "department": "Engineering"},
        {"id": 2, "name": "Sarah", "department": "Marketing"}
    ]

    return jsonify({
    "employees": employees
}), 200