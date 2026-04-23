from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PROCESSING_URL = os.getenv(
    "PROCESSING_URL",
    "https://processing-campus-service-eutmintwgr.cn-beijing.fcapp.run"
)

@app.route("/", methods=["POST"])
def main():
    try:
        data = request.get_json(silent=True) or {}
        submission_id = data.get("submission_id")

        if not submission_id:
            return jsonify({"error": "missing submission_id"}), 400

        payload = {"submission_id": submission_id}
        resp = requests.post(PROCESSING_URL, json=payload, timeout=10)

        return jsonify({
            "message": "processing triggered",
            "submission_id": submission_id,
            "processing_status": resp.status_code
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(environ, start_response):
    return app(environ, start_response)

