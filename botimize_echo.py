import os
import requests

from botimize import Botimize 
from flask import Flask, request

app = Flask(__name__)
 
ACCESS_TOKEN = 'EAAYZCSs2uV0sBAFvOcMBGPOtSzTnEJQ6Jpp36UFZC40qcH0noQSiWubjTzkOvyfU1uOQfH7ZCYb5mrZApv72WEWDjBCBpwyn7bKnMNhKGByZCzZAnLZCQMk9ZCbsOrWnLkddKc9lLCdSOC2OlYzFBiZAoSAMkNMM8XZC1OQXdt9yFcTAZDZD' 
botimize = Botimize('7WAYASBD1MA9LRSUMJ5EZWA7K40P6RRY', 'facebook')
 
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

@app.route('/', methods=['GET'])
def verify():
    return request.args['hub.challenge']
 
@app.route('/', methods=['POST'])
def handle_incoming_messages():

    # incoming
    data = request.json
    botimize.log_incoming(data)

    #outgoing
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message[::-1])
    data_out = {
        "recipient": {"id": sender},
        "message": {"text": message}
    }
    botimize.log_outgoing(data_out)
 
if __name__ == '__main__':
    app.run(debug=True)
