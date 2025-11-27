import os
from flask import Flask, request, send_file
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials from Railway environment variables
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_NUMBER")
my_phone = os.environ.get("MY_PHONE")

client = Client(account_sid, auth_token)
REPLY_FILE = "replies.txt"

# Routes for HTML pages
@app.route('/')
def index():
    return send_file("index.html")

@app.route('/insta')
def insta():
    return send_file("insta.html")

@app.route('/message')
def message():
    return send_file("message.html")

@app.route('/reply')
def reply():
    return send_file("reply.html")

# Endpoint for Twilio message
@app.route('/send', methods=['POST'])
def send_reply():
    data = request.json
    message_text = data.get('message')

    if not message_text:
        return {"error": "No message provided"}, 400

    # Send SMS via Twilio
    try:
        client.messages.create(
            body=f"New reply from webpage: {message_text}",
            from_=twilio_number,
            to=my_phone
        )
    except Exception as e:
        return {"error": str(e)}, 500

    # Save reply locally
    with open(REPLY_FILE, "a") as f:
        f.write(message_text + "\n")

    return {"success": True}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
