import json
from flask import Flask, request
import os

app = Flask(__name__)

# JSON file to store data
DATA_FILE = 'data.json'

# Function to check if JSON file exists, and create it if not
def check_json_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)

@app.route('/save_data', methods=['POST'])
def save_data():
    payload = json.loads(request.data)
    name = payload['name']
    scope = payload['scope']
    key = payload['key']
    value = payload['value']

    # Load existing data from the JSON file
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Create scope and name if not exist
    if scope not in data:
        data[scope] = {}
    if name not in data[scope]:
        data[scope][name] = {}

    # Save data to the JSON file
    data[scope][name][key] = value

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    print(f'Saving data: name={name}, scope={scope}, key={key}, value={value}')
    return json.dumps({'success': True})

@app.route('/get_data', methods=['POST'])
def get_data():
    payload = json.loads(request.data)
    name = payload['name']
    scope = payload['scope']
    key = payload['key']

    # Load data from the JSON file
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Retrieve data from the JSON file
    if scope in data and name in data[scope] and key in data[scope][name]:
        value = data[scope][name][key]
    else:
        value = None

    print(f'Getting data: name={name}, scope={scope}, key={key}, value={value}')

    # Return the retrieved value or None
    return json.dumps({'value': value})

if __name__ == '__main__':
    check_json_file() # Check if JSON file exists and create if not
    app.run(port=8001, debug=True)
