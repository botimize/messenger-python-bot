import os
import sys
import json

import requests
from botimize import Botimize
from flask import Flask, request

app = Flask(__name__)

Botimize_Api_Key = 'Your_Botimize_Api_Key'
FACEBOOK_ACCESS_TOKEN = 'Your_Facebook_Access_Token' 
botimize = Botimize(Botimize_Api_Key, 'facebook')

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json() # receive the message from facebook
    botimize.log_incoming(data) # send incoming message to botimize
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    message_text = messaging_event["message"]["text"]
                    send_message(sender_id, message_text) # send response message to facebook
                    data_out = {
                        "access_token": FACEBOOK_ACCESS_TOKEN,
                        "message": messaging_event["message"],
                        "recipient": messaging_event["sender"]
                    }
                    botimize.log_outgoing(data_out) # send outgoging message to botimize
                else:
                    pass
    return "ok", 200

def send_message(recipient_id, message_text):
    params = {
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

if __name__ == '__main__':
    app.run(debug=True)
