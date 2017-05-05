import os
import requests

from botimize import Botimize 
from flask import Flask, request

app = Flask(__name__)
 
FACEBOOK_ACCESS_TOKEN = 'Your_Facebook_Access_Token'
Botimize_Api_Key = 'Your_Botimize_Api_Key'
botimize = Botimize(Botimize_Api_Key, 'facebook')
 
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + FACEBOOK_ACCESS_TOKEN, json=data)
    return "ok"

@app.route('/', methods=['GET'])
def verify():
    return request.args['hub.challenge']
 
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    # reply
    data_in = request.json
    sender = data_in['entry'][0]['messaging'][0]['sender']['id']
    message = data_in['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message)

    # incoming
    botimize.log_incoming(data_in)

    #outgoing
    data_out = {
        "recipient": {"id": sender},
        "message": {"text": message}
    }
    botimize.log_outgoing(data_out)
    return "ok"
 
if __name__ == '__main__':
    app.run(debug=True)
