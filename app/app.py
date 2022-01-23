from flask import Flask
from flask_sock import Sock
from chat import call_chatbot

app = Flask(__name__)
app.debug = True
sock = Sock(app)


@sock.route('/reverse')
def reverse(ws):
    while True:
        call_chatbot(ws)
        # text = ws.receive()
        # ws.send(text[::-1])
