from flask import Flask, jsonify, request, abort
import uuid, json, os

app = Flask(__name__)

# 📄 Cesta k souboru s uživateli
DATA_FILE = "data/users.json"

# 📥 Načti data ze souboru (pokud existuje), jinak prázdný seznam
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = { "users": [] }

# 💾 Ulož aktuální stav uživatelů do JSON souboru
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ✅ Základní endpoint pro kontrolu, že API běží
@app.route("/")
def home():
    return "API is running!"

# 📋 Získání seznamu všech uživatelů
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(data["users"])

# ➕ Přidání nového uživatele
@app.route("/users", methods=["POST"])
def add_user():
    new_user = request.json
    required_fields = ["name"]

    for field in required_fields:
        if field not in new_user:
            return jsonify({
                "error": {
                    "error_description": f"Missing required field: '{field}'"
                }
            }), 400

    user_id = str(uuid.uuid4())

    user_with_id = {
        "id": user_id,
        "name": new_user["name"],
        "email": new_user.get("email", ""),
        "country": new_user.get("country", ""),
        "age": new_user.get("age", ""),
        "job": new_user.get("job", ""),
        "hobbies": new_user.get("hobbies", "")
    }

    data["users"].append(user_with_id)
    save_data()

    return jsonify({
        "message": "User added",
        "id": user_id
    }), 201

# 🔎 Získání konkrétního uživatele podle ID
@app.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({
        "error": {
            "error_description": f"User with id '{user_id}' not found"
        }
    }), 404

# ❌ Smazání uživatele podle ID
@app.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global data
    user = next((u for u in data["users"] if u["id"] == user_id), None)

    if not user:
        return jsonify({
            "error": {
                "error_description": f"User with id '{user_id}' not found"
            }
        }), 404

    data["users"] = [u for u in data["users"] if u["id"] != user_id]
    save_data()
    return '', 204

# 🚨 Globální handler pro neočekávané chyby
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "error": {
            "error_description": str(e)
        }
    }), 500

# ▶️ Spuštění aplikace
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
