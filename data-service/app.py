from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = '/data/records.json'

# make sure data dic exist
os.makedirs('/data', exist_ok=True)

def load_records():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_records(records):
    with open(DATA_FILE, 'w') as f:
        json.dump(records, f, indent=2)

@app.route('/records', methods=['POST'])
def create_record():
    data = request.json
    record_id = data.get('id')
    records = load_records()
    records[record_id] = data
    save_records(records)
    return jsonify({'status': 'created', 'id': record_id}), 201

@app.route('/records/<record_id>', methods=['GET'])
def get_record(record_id):
    records = load_records()
    if record_id not in records:
        return jsonify({'error': 'not found'}), 404
    return jsonify(records[record_id])

@app.route('/records/<record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.json
    records = load_records()
    if record_id not in records:
        return jsonify({'error': 'not found'}), 404
    records[record_id].update(data)
    save_records(records)
    return jsonify(records[record_id])

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)