import json
from quart import Quart, request, jsonify

app = Quart(__name__)

# Route for saving data to the server
@app.route('/save', methods=['POST'])
async def save():
    try:
        data = await request.get_json()
        store_name = data.get('storeName')
        store_scope = data.get('storeScope')
        key = data.get('key')
        value = data.get('value')

        # Create a dictionary to store the data
        store_data = {}
        store_data['storeName'] = store_name
        store_data['storeScope'] = store_scope
        store_data['data'] = {}

        # Check if the JSON file exists, if not, create it
        try:
            with open('data.json', 'r') as f:
                store_data = json.load(f)
        except FileNotFoundError:
            with open('data.json', 'w') as f:
                json.dump(store_data, f)

        # Save the data to the JSON file
        with open('data.json', 'r+') as f:
            store_data = json.load(f)
            if store_name not in store_data['data']:
                store_data['data'][store_name] = {}
            if store_scope not in store_data['data'][store_name]:
                store_data['data'][store_name][store_scope] = {}
            store_data['data'][store_name][store_scope][key] = value
            f.seek(0)
            json.dump(store_data, f)
            f.truncate()

        # Return a JSON response indicating success
        response = {
            'success': True
        }
        return jsonify(response)

    except Exception as e:
        # Return a JSON response indicating failure with an error message
        response = {
            'success': False,
            'error': str(e)
        }
        return jsonify(response), 500

# Route for loading data from the server
@app.route('/load', methods=['POST'])
async def load():
    try:
        data = await request.get_json()
        store_name = data.get('storeName')
        store_scope = data.get('storeScope')
        key = data.get('key')

        # Load the data from the JSON file
        with open('data.json', 'r') as f:
            store_data = json.load(f)
            value = store_data['data'].get(store_name, {}).get(store_scope, {}).get(key)

        # Return a JSON response with the loaded data
        response = {
            'success': True,
            'value': value
        }
        return jsonify(response)

    except Exception as e:
        # Return a JSON response indicating failure with an error message
        response = {
            'success': False,
            'error': str(e)
        }
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True, port=8001)  # Run the Quart app in debug mode on port 8001 for development