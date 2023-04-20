import json
from flask import Flask, request
## Signed By ARD on 20/04/2023 just 10 days before his birthday on 19:47 IST
app = Flask(__name__)

# JSON file to store data
DATA_FILE = 'data.json'

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
    
    # Save data to the JSON file
    if scope not in data:
        data[scope] = {}
    if name not in data[scope]:
        data[scope][name] = {}
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
    app.run(port=8001, debug=True)
