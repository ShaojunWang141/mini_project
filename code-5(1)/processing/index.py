from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://123.57.211.134:5002")
RESULT_FUNCTION_URL = os.getenv(
    "RESULT_FUNCTION_URL",
    "https://result-update-tljnltwqoi.cn-beijing.fcapp.run"
)

def check_required_fields(record):
    required = ["title", "description", "location", "date", "organizer"]
    return all(record.get(field) for field in required)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except Exception:
        return False

def determine_category(title, description):
    text = f"{title} {description}".lower()
    if any(kw in text for kw in ["career", "internship", "recruitment"]):
        return "OPPORTUNITY"
    elif any(kw in text for kw in ["workshop", "seminar", "lecture"]):
        return "ACADEMIC"
    elif any(kw in text for kw in ["club", "society", "social"]):
        return "SOCIAL"
    return "GENERAL"

def determine_priority(category):
    if category == "OPPORTUNITY":
        return "HIGH"
    elif category == "ACADEMIC":
        return "MEDIUM"
    return "NORMAL"

def generate_note(status, category, priority):
    if status == "INCOMPLETE":
        return "Missing required fields. Please fill all fields."
    elif status == "NEEDS_REVISION":
        return "Please check date format (YYYY-MM-DD) and ensure description is at least 40 characters."
    return f"Approved as {category} event with {priority} priority."

@app.route("/", methods=["POST"])
def main():
    try:
        body = request.get_json(silent=True) or {}
        submission_id = body.get("submission_id")

        if not submission_id:
            return jsonify({"error": "missing submission_id"}), 400

        resp = requests.get(f"{DATA_SERVICE_URL}/records/{submission_id}", timeout=10)
        if resp.status_code != 200:
            return jsonify({"error": f"record not found, status: {resp.status_code}"}), 500

        record = resp.json()

        if not check_required_fields(record):
            status = "INCOMPLETE"
            category = None
            priority = None
        elif (not validate_date(record["date"])) or len(record["description"]) < 40:
            status = "NEEDS_REVISION"
            category = None
            priority = None
        else:
            status = "APPROVED"
            category = determine_category(record["title"], record["description"])
            priority = determine_priority(category)

        note = generate_note(status, category, priority)

        result_data = {
            "submission_id": submission_id,
            "status": status,
            "category": category,
            "priority": priority,
            "note": note
        }

        update_resp = requests.post(RESULT_FUNCTION_URL, json=result_data, timeout=10)

        return jsonify({
            "message": "processed",
            "submission_id": submission_id,
            "status": status,
            "update_status": update_resp.status_code
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(environ, start_response):
    return app(environ, start_response)
