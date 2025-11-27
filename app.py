import os
from flask import Flask, request, send_file
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials from Railway environment variables
account_sid = os.environ.get("AC4ffbe0800b709f18e98becabae5a9f85")
auth_token = os.environ.get("a23794664749d9e023627ab56ad09fc8")
twilio_number = os.environ.get("+14122930656")
my_phone = os.environ.get("+919006110746")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
