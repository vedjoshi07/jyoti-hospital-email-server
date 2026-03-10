from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

RESEND_API_KEY = "re_Fet1qKFp_7zwVj57135qjmF7vTHtfeghs"


@app.route("/send-email", methods=["POST"])
def send_email():

    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No JSON provided"}), 400

    to_email = data.get("to")
    subject = data.get("subject")
    body = data.get("body")

    if not to_email or not subject or not body:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    try:

        url = "https://api.resend.com/emails"

        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "from": "Jyoti Eye Hospital <onboarding@resend.dev>",
            "to": [to_email],
            "subject": subject,
            "html": body
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in [200, 201]:

            return jsonify({
                "status": "success",
                "message": "Email sent successfully"
            })

        else:

            return jsonify({
                "status": "error",
                "message": response.text
            }), 500

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/")
def home():
    return "Jyoti Hospital Email Server Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
