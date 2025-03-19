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
    name = request.form.get("name")  # Get form data
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        return jsonify({"error": "Missing form fields"}), 400

    return jsonify({"message": "Form received!", "name": name, "email": email, "message": message}), 200


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
