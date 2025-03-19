from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Email configuration
EMAIL_ADDRESS = "your_email@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "your_email_password"  # Use an app password if using Gmail

@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        data = request.json  # Get JSON data from frontend
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        # Create email content
        email_msg = EmailMessage()
        email_msg["Subject"] = "New Contact Form Submission"
        email_msg["From"] = EMAIL_ADDRESS
        email_msg["To"] = EMAIL_ADDRESS  # Send to yourself
        email_msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(email_msg)

        return jsonify({"message": "Message sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
