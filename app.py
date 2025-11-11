from flask import Flask, request, jsonify
import requests
import os, json

app = Flask(__name__)

GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbwxqh7D_lorKQL5PmR2m6vnNxeuXFb31ZfB98mwFIQ6UbEkKhqxp8zAUriNFlH_IOx7NA/exec"

@app.route("/", methods=["POST"])
def receive_json():
    try:
        # Parse JSON even if header is wrong
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "No JSON payload received"}), 400

        # If it's wrapped like {"raw":"{...}"}, unwrap and decode it
        if "raw" in data and isinstance(data["raw"], str):
            try:
                data = json.loads(data["raw"])
            except Exception as e:
                print("Failed to decode raw JSON:", e)

        # Normalize keys to lowercase so it ignores Title/title/etc.
        normalized = {k.lower(): v for k, v in data.items()}
        print("Received JSON:", normalized)

        # Forward clean JSON to Google Apps Script
        response = requests.post(
            GOOGLE_SHEET_WEBHOOK,
            json=normalized,
            headers={"Content-Type": "application/json"}
        )

        print("Forwarded to Google Apps Script. Status:", response.status_code)
        print("Response text:", response.text)

        return jsonify({
            "status": "success",
            "forward_status": response.status_code,
            "forward_response": response.text
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Marketplace Sheet Writer is live."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
