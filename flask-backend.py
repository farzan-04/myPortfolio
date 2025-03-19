from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Email configuration
EMAIL_ADDRESS = "mohammedfarzan04@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "Farzan04@portfolio"  # Use an App Password for security

@app.route("/")
def home():
    return render_template("index.html")  # Load the HTML page

@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        # Try to get form data (from HTML form)
        if request.form:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

        # Try to get JSON data (from JavaScript fetch)
        elif request.is_json:
            data = request.get_json()
            name = data.get("name")
            email = data.get("email")
            message = data.get("message")

        else:
            return jsonify({"error": "Invalid request format"}), 400

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

        return redirect(url_for("success"))  # Redirect to success page
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/success")
def success():
    return "Your message has been sent successfully! ✅"

if __name__ == "__main__":
    app.run(debug=True)
