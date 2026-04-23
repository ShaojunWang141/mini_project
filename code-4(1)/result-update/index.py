from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://123.57.211.134:5002")

@app.route("/", methods=["POST"])
def main():
    try:
        data = request.get_json(silent=True) or {}
        submission_id = data.get("submission_id")

        if not submission_id:
            return jsonify({"error": "missing submission_id"}), 400

        update_data = {
            "status": data.get("status"),
            "category": data.get("category"),
            "priority": data.get("priority"),
            "note": data.get("note")
        }

        resp = requests.put(
            f"{DATA_SERVICE_URL}/records/{submission_id}",
            json=update_data,
            timeout=10
        )

        if resp.status_code == 200:
            return jsonify({"message": "updated successfully"}), 200

        return jsonify({"error": "update failed", "status": resp.status_code}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(environ, start_response):
    return app(environ, start_response)
