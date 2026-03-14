from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import Config
from app.employees import employees_bp
from app.analytics import analytics_bp
from app.auth import generate_token

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

app.register_blueprint(employees_bp, url_prefix="/employees")
app.register_blueprint(analytics_bp, url_prefix="/analytics")


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/auth/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "gollareshma":

        token = generate_token(username, "admin")

        return jsonify({
            "token": token
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)