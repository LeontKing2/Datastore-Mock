from flask import Flask, request, jsonify

app = Flask(__name__)

# Datastore to store key-value pairs
datastore = {}

@app.route('/datastore/set', methods=['POST'])
def set_data():
    key = request.form.get('key')
    value = request.form.get('value')
    if key is not None and value is not None:
        datastore[key] = value
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
        return 'OK', 200
    else:
        return 'Bad Request', 400

@app.route('/datastore/remove', methods=['POST'])
def remove_data():
    key = request.form.get('key')
    if key is not None and key in datastore:
        del datastore[key]
        return 'OK', 200
    else:
        return 'Not Found', 404

if __name__ == '__main__':
    app.run(host='localhost', port=8001)
