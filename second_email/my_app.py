from flask import Flask, request
import json
app = Flask(__name__)

import hashlib, hmac

from mail import api, sendHtmlMessage

@app.route('/', methods=['POST', 'GET'])
def index():
    print "headers = {}".format(str(request.headers))
    print "args = {}".format(str(request.args))
    print "form = {}".format(str(request.form))
    print "data = {}".format(str(request.data))
    print "json = {}".format(str(request.json))
    data = request.form

    token = data.get('token')
    timestamp = data.get('timestamp')
    signature = data.get('signature')
    event = data.get('event')
    if not token or not timestamp or not signature or not event:
        return "Bad request",406

    if not verify(api, token, timestamp, signature):
        return "Request not authorized", 406
        

    if event == 'clicked':
        clickedUrl = data.get('url')
        recipient = data.get('recipient')
        # add checks on the basis of url that is clicked
        if clickedUrl:
            sendHtmlMessage(recipient, subject="follow up")
    return "Hello, world!", 200


def verify(api_key, token, timestamp, signature):
    hmac_digest = hmac.new(key=api_key,
                           msg='{}{}'.format(timestamp, token),
                           digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(unicode(signature), unicode(hmac_digest))

if __name__ == '__main__':
    app.run()