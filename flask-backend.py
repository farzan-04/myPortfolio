from flask import Flask, request, render_template, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

@app.route("/")
def home():
    return render_template("index.html")  # Load the HTML page

@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        print("📥 Received request!")  # Debugging log

        print("🔍 Form Data:", request.form)  # Print the received form data

        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            print("❌ Missing field detected!")  # Debugging log
            return jsonify({"error": "Missing form fields"}), 400

        # Create email content
        email_msg = EmailMessage()
        email_msg["Subject"] = "New Contact Form Submission"
        email_msg["From"] = EMAIL_ADDRESS
        email_msg["To"] = EMAIL_ADDRESS
        email_msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")

        # Send email securely
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(email_msg)

        return jsonify({"message": "Your message has been sent successfully!"}), 200

    except Exception as e:
        print("⚠️ Error:", str(e))  # Debugging log
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
