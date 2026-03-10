from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Note: In a production environment, use environment variables or a config file
SMTP_HOST: str = "smtp.gmail.com"
SMTP_PORT: int = 587
SMTP_USER: str = "joshived777@gmail.com" 
SMTP_PASS: str = "fdll iooo hqwl utpv"         # MUST be a 16-character Google App Password

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400
        
    to_email: str = data.get('to', '')
    subject: str = data.get('subject', '')
    body: str = data.get('body', '')

    if not to_email or not subject or not body:
        return jsonify({"status": "error", "message": "Missing required fields (to, subject, body)"}), 400

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        return jsonify({"status": "success", "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Running on port 5001 as per user request
    app.run(port=5001, debug=True)
