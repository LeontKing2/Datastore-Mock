from quart import Quart, request, jsonify
import json
import sqlite3

app = Quart(__name__)

# Endpoint for loading data
@app.route('/load', methods=['POST'])
async def load_data():
    data = await request.json
    store_name = data['storeName']
    store_scope = data['storeScope']
    key = data['key']
    
    # Load data from JSON file or SQLite database based on store_scope
    if store_scope == 'global':
        with open('./global_data.json', 'r') as f:
            global_data = json.load(f)
        value = global_data.get(key)
    elif store_scope == 'local':
        conn = sqlite3.connect('./local_data.db')
        cursor = conn.cursor()
        cursor.execute("./SELECT value FROM local_data WHERE store_name=? AND key=?", (store_name, key))
        result = cursor.fetchone()
        value = result[0] if result else None
        conn.close()
    else:
        return jsonify({'success': False, 'error': 'Invalid storeScope'})
    
    return jsonify({'success': True, 'value': value})

# Endpoint for saving data
@app.route('/save', methods=['POST'])
async def save_data():
    data = await request.json
    store_name = data['storeName']
    store_scope = data['storeScope']
    key = data['key']
    value = data['value']
    
    # Save data to JSON file or SQLite database based on store_scope
    if store_scope == 'global':
        with open('./global_data.json', 'r') as f:
            global_data = json.load(f)
        global_data[key] = value
        with open('./global_data.json', 'w') as f:
            json.dump(global_data, f)
    elif store_scope == 'local':
        conn = sqlite3.connect('./local_data.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS local_data (store_name TEXT, key TEXT, value TEXT)")
        cursor.execute("INSERT OR REPLACE INTO local_data (store_name, key, value) VALUES (?, ?, ?)", (store_name, key, value))
        conn.commit()
        conn.close()
    else:
        return jsonify({'success': False, 'error': 'Invalid storeScope'})
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=8001)