from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
import os

# set up Flask
app = Flask(__name__)
# set up Twilio client
ACCOUNT_SID = "ACbbdfbb7ce1a4a179eb0ce3a5987f47c5"
AUTH_TOKEN = "7905742cf5c12867c9097390302db43a"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# Try adding your own number to this list!
callers = {
    "+14158675309": "Curious George",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
    "+12819196619": "Tyler",
    "+12814509485": "Denise",
}

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        message = "Monkey, thanks for the message!"

    resp = twilio.twiml.Response()
    resp.message(message)

    # message = client.sms.messages.create(to="+12814509485",
    #         from_="+18327722167",
    #         body="Hello there!")

    print str(resp)
    return str(resp)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
