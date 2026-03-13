<<<<<<< HEAD
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import Config
from app.employees import employees_bp
from app.analytics import analytics_bp
from app.auth import generate_token, USERS
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# MySQL connection
mysql = MySQL(app)

# Attach mysql to blueprints
employees_bp.mysql = mysql
analytics_bp.mysql = mysql

# Register APIs
app.register_blueprint(employees_bp, url_prefix="/employees")
app.register_blueprint(analytics_bp, url_prefix="/analytics")


# Login endpoint
@app.route("/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = USERS.get(username)

    if not user or user["password"] != password:
        logger.warning(f"Failed login attempt: {username}")
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(username, user["role"])

    logger.info(f"Successful login: {username}")

    return jsonify({
        "message": "Login successful",
        "token": token,
        "role": user["role"]
    }), 200


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception as e:

        return jsonify({
            "status": "unhealthy",
            "database": str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

=======
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Employee API is running"})

@app.route('/employees')
def employees():
    data = [
        {"id": 1, "name": "Alice", "role": "Developer"},
        {"id": 2, "name": "Bob", "role": "DevOps Engineer"}
    ]
    return jsonify(data)
>>>>>>> 5e834299faeb7c132b7ff092595e7d6211840acd

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)