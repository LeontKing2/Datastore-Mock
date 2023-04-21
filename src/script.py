import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# File to store the data
DATASTORE_FILE = 'datastore.json'

# Load initial data from the file
try:
    with open(DATASTORE_FILE, 'r') as f:
        datastore = json.load(f)
except FileNotFoundError:
    datastore = {}

@app.route('/datastore', methods=['POST'])
def datastore_endpoint():
    try:
        data = request.json
        method = data['method']
        key = data['key']
        if method == 'SetAsync':
            value = data['value']
            datastore[key] = value
            with open(DATASTORE_FILE, 'w') as f:
                json.dump(datastore, f)
            return jsonify({'success': True})
        elif method == 'GetAsync':
            value = datastore.get(key)
            return jsonify({'success': True, 'value': value})
        elif method == 'UpdateAsync':
            transform_func = data['transform_func']
            if key in datastore:
                value = datastore[key]
                new_value = transform_func(value)
                datastore[key] = new_value
                with open(DATASTORE_FILE, 'w') as f:
                    json.dump(datastore, f)
                return jsonify({'success': True, 'value': new_value})
            else:
                return jsonify({'success': False, 'error': 'Key not found'})
        elif method == 'RemoveAsync':
            if key in datastore:
                del datastore[key]
                with open(DATASTORE_FILE, 'w') as f:
                    json.dump(datastore, f)
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Key not found'})
        else:
            return jsonify({'success': False, 'error': 'Invalid method'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(port=8001, debug=True)
