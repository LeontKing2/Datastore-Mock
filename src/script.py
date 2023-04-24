from quart import Quart, request, jsonify
import json
import sqlite3

app = Quart(__name__)

# Connect to SQLite database
conn = sqlite3.connect('datastore.db')
c = conn.cursor()

# Create a table for data storage
c.execute('''CREATE TABLE IF NOT EXISTS data_store
             (key TEXT PRIMARY KEY, value TEXT)''')
conn.commit()

# Create a JSON file if missing
try:
    with open('datastore.json', 'r') as f:
        pass
except FileNotFoundError:
    with open('datastore.json', 'w') as f:
        json.dump({}, f)

@app.route('/datastore', methods=['POST'])
async def store_data():
    try:
        data = await request.get_json()
        if 'key' not in data or 'value' not in data:
            return 'Error: Invalid payload', 400

        key = data['key']
        value = data['value']

        # Store data in JSON file
        with open('datastore.json', 'r+') as f:
            datastore = json.load(f)
            datastore[key] = value
            f.seek(0)
            json.dump(datastore, f, indent=4)

        # Store data in SQLite database
        c.execute("INSERT OR REPLACE INTO data_store (key, value) VALUES (?, ?)",
                  (key, json.dumps(value)))
        conn.commit()

        return 'Success', 200
    except Exception as e:
        return f'Error: {e}', 500


@app.route('/datastore/<key>', methods=['GET'])
async def get_data(key):
    try:
        # Retrieve data from JSON file
        with open('datastore.json', 'r') as f:
            datastore = json.load(f)
            value_json = datastore.get(key)

        # Retrieve data from SQLite database
        c.execute("SELECT value FROM data_store WHERE key=?", (key,))
        value_db = c.fetchone()

        if value_json is None and value_db is None:
            return 'Error: Key not found', 404

        # Return data as JSON
        return jsonify({'key': key, 'value_json': value_json, 'value_db': json.loads(value_db[0])}), 200
    except Exception as e:
        return f'Error: {e}', 500


if __name__ == '__main__':
    app.run(debug=True)