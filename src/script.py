from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# File path to store data in JSON format
datastore_file = 'datastore.json'

# Load initial data from JSON file
try:
    with open(datastore_file, 'r') as file:
        datastore = json.load(file)
except FileNotFoundError:
    datastore = {}

@app.route('/datastore/set', methods=['POST'])
def set_data():
    key = request.form.get('key')
    value = request.form.get('value')
    if key is not None and value is not None:
        datastore[key] = value
        save_datastore_to_file()
        return 'OK', 200
    else:
        return 'Bad Request', 400

@app.route('/datastore/get', methods=['GET'])
def get_data():
    key = request.args.get('key')
    if key is not None and key in datastore:
        return jsonify({'value': datastore[key]}), 200
    else:
        return 'Not Found', 404

@app.route('/datastore/update', methods=['POST'])
def update_data():
    key = request.form.get('key')
    value = request.form.get('value')
    if key is not None and key in datastore and value is not None:
        current_value = datastore[key]
        current_value.update(value)
        datastore[key] = current_value
        save_datastore_to_file()
        return 'OK', 200
    else:
        return 'Bad Request', 400

@app.route('/datastore/remove', methods=['POST'])
def remove_data():
    key = request.form.get('key')
    if key is not None and key in datastore:
        del datastore[key]
        save_datastore_to_file()
        return 'OK', 200
    else:
        return 'Not Found', 404

def save_datastore_to_file():
    with open(datastore_file, 'w') as file:
        json.dump(datastore, file)

if __name__ == '__main__':
    app.run(host='localhost', port=8001)
