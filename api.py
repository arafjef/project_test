from flask import Flask, jsonify, request

app = Flask(__name__)

data = {
    "users": []
}

@app.route("/")
def home():
    return "API is running!"

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(data["users"])

@app.route("/users", methods=["POST"])
def add_user():
    new_user = request.json
    data["users"].append(new_user)
    return jsonify({"message": "User added"}), 201

@app.route("/users/<string:name>", methods=["GET"])
def get_user(name):
    user = next((u for u in data["users"] if u["name"] == name), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
