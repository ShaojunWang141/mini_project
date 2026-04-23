from flask import Flask, request, jsonify
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import uuid
import os

app = Flask(__name__)

DATA_SERVICE_URL = os.getenv('DATA_SERVICE_URL', 'http://data-service:5002')
EVENT_FUNCTION_URL = os.getenv('EVENT_FUNCTION_URL', 'https://submisson-event-duokthrmmt.cn-beijing.fcapp.run')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    

    record_id = str(uuid.uuid4())
    

    record = {
        'id': record_id,
        'status': 'PENDING',
        'title': data.get('title'),
        'description': data.get('description'),
        'location': data.get('location'),
        'date': data.get('date'),
        'organizer': data.get('organizer')
    }
    

    resp = requests.post(f'{DATA_SERVICE_URL}/records', json=record)
    if resp.status_code != 201:
        return jsonify({'error': 'failed to save'}), 500
    

    if EVENT_FUNCTION_URL:
        try:
            print(f"[DEBUG] Calling function: {EVENT_FUNCTION_URL}", flush=True)
            event_url = EVENT_FUNCTION_URL.rstrip('/') + '/'

            func_resp = requests.post(
                event_url,
                json={'submission_id': record_id},
                headers={'Content-Type': 'application/json'},
                timeout=10,
                verify=False
            )
            print(f"[DEBUG] Function response: {func_resp.status_code} - {func_resp.text}", flush=True)
        except Exception as e:
            print(f"[ERROR] Failed to trigger function: {e}", flush=True)
    else:
        print("[WARN] EVENT_FUNCTION_URL is not set!", flush=True)
    
    return jsonify({'id': record_id, 'status': 'PENDING'})

@app.route('/result/<record_id>', methods=['GET'])
def get_result(record_id):
    resp = requests.get(f'{DATA_SERVICE_URL}/records/{record_id}')
    if resp.status_code != 200:
        return jsonify({'error': 'not found'}), 404
    
    record = resp.json()
    return jsonify({
        'id': record['id'],
        'status': record.get('status'),
        'category': record.get('category'),
        'priority': record.get('priority'),
        'note': record.get('note')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)