import json
from quart import Quart, request, jsonify
import pyodbc
import sqlite3

#Storage Types = sqlite, sql_server, json
storage_type="json"


def save_to_sql_server(store_name, store_scope, key, value):
    # Establish a connection to SQL Server
    # Make sure to specify the SQL driver you will be using or pyodbc will be confused af lol
    # also yeah make sure to specify the database, UID(Userid), PWD(Password) your welcome!
    conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=<your_server_name>;'
                          'DATABASE=<your_database_name>;'
                          'UID=<your_username>;'
                          'PWD=<your_password>')

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to insert data into the table
    query = f"INSERT INTO {store_name} (store_scope, key, value) VALUES (?, ?, ?)"
    cursor.execute(query, (store_scope, key, value))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Function to load data from SQL Server
def load_from_sql_server(store_name, store_scope, key):
    # Establish a connection to SQL Server
    conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=<your_server_name>;'
                          'DATABASE=<your_database_name>;'
                          'UID=<your_username>;'
                          'PWD=<your_password>')

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to select data from the table
    query = f"SELECT value FROM {store_name} WHERE store_scope=? AND key=?"
    cursor.execute(query, (store_scope, key))

    # Fetch the result and close the connection
    result = cursor.fetchone()
    conn.close()

    # Return the value if found, otherwise return None
    return result[0] if result else None

# Function to save data to JSON file
def save_to_json(store_name, store_scope, key, value):
    # Load the existing JSON file into memory
    with open(f"{store_name}.json", 'r') as file:
        data = json.load(file)

    # Update the data with the new key-value pair
    if store_scope not in data:
        data[store_scope] = {}
    data[store_scope][key] = value

    # Write the updated data back to the JSON file
    with open(f"{store_name}.json", 'w') as file:
        json.dump(data, file)

# Function to load data from JSON file
def load_from_json(store_name, store_scope, key):
    # Load the existing JSON file into memory
    with open(f"{store_name}.json", 'r') as file:
        data = json.load(file)

    # Return the value if found, otherwise return None
    return data.get(store_scope, {}).get(key)

# Function to save data to SQLite database
def save_to_sqlite(store_name, store_scope, key, value):
    # Establish a connection to SQLite database
    conn = sqlite3.connect(f"{store_name}.db")
    cursor = conn.cursor()

    # Construct the SQL query to insert data into the table
    query = f"INSERT INTO {store_name} (store_scope, key, value) VALUES (?, ?, ?)"
    cursor.execute(query, (store_scope, key, value))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Function to load data from SQLite database
def load_from_sqlite(store_name, store_scope, key):
    # Establish a connection to SQLite database
    conn = sqlite3.connect(f"{store_name}.db")
    cursor = conn  # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to select data from the table
    query = f"SELECT value FROM {store_name} WHERE store_scope=? AND key=?"
    cursor.execute(query, (store_scope, key))

    # Fetch the result and close the connection
    result = cursor.fetchone()
    conn.close()

    # Return the value if found, otherwise return None
    return result[0] if result else None

@app.route('/save', methods=['POST'])
async def save():
    try:
        data = await request.get_json()
        store_name = data.get('storeName')
        store_scope = data.get('storeScope')
        key = data.get('key')
        value = data.get('value')

        if storage_type == 'sql_server':
            save_to_sql_server(store_name, store_scope, key, value)
        elif storage_type == 'json':
            save_to_json(store_name, store_scope, key, value)
        elif storage_type == 'sqlite':
            save_to_sqlite(store_name, store_scope, key, value)
        else:
            return jsonify({'error': 'Invalid storage type'})

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)})


# Route for loading data from the server
@app.route('/load', methods=['POST'])
async def load():
    try:
        data = await request.get_json()
        store_name = data.get('storeName')
        store_scope = data.get('storeScope')
        key = data.get('key')

        if storage_type == 'sql_server':
            result = load_from_sql_server(store_name, store_scope, key)
        elif storage_type == 'json':
            result = load_from_json(store_name, store_scope, key)
        elif storage_type == 'sqlite':
            result = load_from_sqlite(store_name, store_scope, key)
        else:
            return jsonify({'error': 'Invalid storage type'})

        return jsonify({'data': result})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=8001)