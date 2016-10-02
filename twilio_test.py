from time import sleep
import datetime
from twilio.rest import TwilioRestClient
from twilio_auth import ACCOUNT_SID, AUTH_TOKEN
from flask import Flask, request, redirect
import twilio.twiml

# set up Flask
# app = Flask(__name__)

# set up Twilio client
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
# message = client.sms.messages.create(to="+12819196619",
#                                      from_="+18327722167",
#                                      body="Hello there!")
now = datetime.datetime.now()
messages = client.messages.list(
    date_sent = datetime.date(now.year,now.month,now.day)
)
messages_length = len(messages)

for message in messages:
    print message.body

while(1):
    print len(messages)
    now = datetime.datetime.now()
    messages = client.messages.list(
        date_sent = datetime.date(now.year,now.month,now.day)
    )
    if len(messages) is not messages_length:
        print "message length wasn't the same!"
        messages_length = len(messages)
        last_message = messages[-1]
        body_mesg = "You said {0}.".format(last_message.body)
        message = client.sms.messages.create(to="+12819196619",
                from_="+18327722167",
                body="Hello there!")
    # only check every 5 seconds to not overload server
    sleep(1)

