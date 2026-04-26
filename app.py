from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import Config
from app.employees import employees_bp
from app.analytics import analytics_bp
from app.auth import generate_token, USERS
import logging

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

try:
    mysql = MySQL(app)
    employees_bp.mysql = mysql
    analytics_bp.mysql = mysql
except Exception as e:
    print("MySQL not available, running in CI mode")

# register routes
app.register_blueprint(employees_bp, url_prefix="/employees")
app.register_blueprint(analytics_bp, url_prefix="/analytics")


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = USERS.get(username)

    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(username, user["role"])

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)