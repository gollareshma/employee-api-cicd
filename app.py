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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)