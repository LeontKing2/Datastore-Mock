from quart import Quart, request, jsonify
import json
import sqlite3

app = Quart(__name__)

# Endpoint for loading data
@app.route('/load', methods=['POST'])
async def load_data():
    data = await request.json
    storeName = data['storeName']
    storeScope = data['storeScope']
    key = data['key']
    
    # Load data from JSON file or SQLite database based on storeScope
    if storeScope == 'global':
        with open('./global_data.json', 'r') as f:
            global_data = json.load(f)
        value = global_data.get(key)
    elif storeScope == 'local':
        conn = sqlite3.connect('./local_data.db')
        cursor = conn.cursor()
        cursor.execute("./SELECT value FROM local_data WHERE storeName=? AND key=?", (storeName, key))
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
    storeName = data['storeName']
    storeScope = data['storeScope']
    key = data['key']
    value = data['value']
    
    # Save data to JSON file or SQLite database based on storeScope
    if storeScope == 'global':
        with open('./global_data.json', 'r') as f:
            global_data = json.load(f)
        global_data[key] = value
        with open('./global_data.json', 'w') as f:
            json.dump(global_data, f)
    elif storeScope == 'local':
        conn = sqlite3.connect('./local_data.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS local_data (storeName TEXT, key TEXT, value TEXT)")
        cursor.execute("INSERT OR REPLACE INTO local_data (storeName, key, value) VALUES (?, ?, ?)", (storeName, key, value))
        conn.commit()
        conn.close()
    else:
        return jsonify({'success': False, 'error': 'Invalid storeScope'})
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=8001)