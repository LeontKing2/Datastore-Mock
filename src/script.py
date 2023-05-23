import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_DIR = "datastore"  # Directory to store the JSON files
PORT = 8002  # Port number for the server

def get_file_path(game_id, key):
    game_dir = os.path.join(DATA_DIR, game_id)
    os.makedirs(game_dir, exist_ok=True)
    file_path = os.path.join(game_dir, key + ".json")
    return file_path

@app.route("/datastore/<game_id>/<key>", methods=["GET"])
def get_data(game_id, key):
    file_path = get_file_path(game_id, key)
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return jsonify(data)
    else:
        return jsonify(None)

@app.route("/datastore/<game_id>/<key>", methods=["POST"])
def set_data(game_id, key):
    data = request.get_json()
    file_path = get_file_path(game_id, key)
    with open(file_path, "w") as file:
        json.dump(data, file)
    return jsonify(data)

@app.route("/datastore/<game_id>/<key>", methods=["DELETE"])
def delete_data(game_id, key):
    file_path = get_file_path(game_id, key)
    if os.path.isfile(file_path):
        os.remove(file_path)
    return jsonify(None)

if __name__ == "__main__":
    app.run(port=PORT)
