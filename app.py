import os
from flask import Flask, request, send_file
from twilio.rest import Client

app = Flask(name)

# Twilio credentials from Railway environment variables
account_sid = os.environ.get("AC2d1ff15cbc93ae35758549ea64c9a146")
auth_token = os.environ.get("28e781f694ac5e9c0bb5d2c5a98a5026")
twilio_number = os.environ.get(" +18287959778")
my_phone = os.environ.get("+919142574197")

client = Client(account_sid, auth_token)
REPLY_FILE = "replies.txt"

@app.route('/')
def home():
    return send_file("reply.html")

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

if name == "main":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
