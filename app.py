from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Google Apps Script Webhook URL (you'll paste this into Render as an environment variable)
GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")

@app.route("/", methods=["POST"])
def receive_data():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    try:
        # Forward the JSON payload to your Google Apps Script
        r = requests.post(GOOGLE_SCRIPT_URL, json=data)
        if r.status_code == 200:
            return jsonify({"status": "success", "sheet_response": r.text}), 200
        else:
            return jsonify({"status": "error", "sheet_response": r.text}), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def health_check():
    return "✅ Sheet Writer Backend is running", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
