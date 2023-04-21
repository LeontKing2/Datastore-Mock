from flask import Flask, request, jsonify
import json

app = Flask(__name__)

DATA_FILE = "datastore.json"  # File to store data

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/save_data', methods=['POST'])
def save_data_route():
    payload = request.get_json()
    name = payload['name']
    scope = payload['scope']
    key = payload['key']
    value = payload['value']

    data = load_data()

    if scope not in data:
        data[scope] = {}
    if name not in data[scope]:
        data[scope][name] = {}

    # Update value instead of duplicating
    data[scope][name][key] = value

    save_data(data)

    return jsonify({'success': True})

@app.route('/get_data', methods=['POST'])
def get_data_route():
    payload = request.get_json()
    name = payload['name']
    scope = payload['scope']
    key = payload['key']

    data = load_data()

    value = data.get(scope, {}).get(name, {}).get(key)

    return jsonify({'value': value})

if __name__ == '__main__':
    app.run(debug=True, port=8001)
