import sys
from wit import Wit
import wikipedia
from twilio.rest import TwilioRestClient
from twilio_auth import ACCOUNT_SID, AUTH_TOKEN

# set up Twilio client
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
message = client.sms.messages.create(to="+12819196619",
                                     from_="+18327722167",
                                     body="Hello there!")

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def last_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][-1]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    print(response['text'])

def get_article(request):
    context = request['context']
    entities = request['entities']

    print 'entities is: ', entities

    wikipedia_search_query = last_entity_value(entities, 
            'wikipedia_search_query')
    if wikipedia_search_query:
        try:
            context['summary'] = wikipedia.summary(wikipedia_search_query)
        except wikipedia.exceptions.DisambiguationError as e:
            emesg = "{0} could refer to multiple things. "
            emesg = emesg.format(wikipedia_search_query)
            # emesg += "Try asking for 'Wikipedia {1}', or "
            emesg += "Try asking for "
            for option in e.options:
                emesg += "'Wikipedia {0}', or ".format(option)
            emesg = emesg[:-4]
            context['errorMessage'] = emesg
            # context['disambiguation_options'] = e.options
        except wikipedia.exceptions.PageError as e:
            emesg = "Can't find a page for {0}. "
            emesg += "Perhaps try 'Wikipedia {0}' or a different search term altogether."
            emesg = emesg.format(wikipedia_search_query)
            context['errorMessage'] = emesg

        if context.get('missingSearchQuery') is not None:
            del context['missingSearchQuery']
    else:
        context['missingSearchQuery'] = True
        if context.get('summary') is not None:
            del context['summary']
        if context.get('errorMessage') is not None:
            del context['errorMessage']

    # print 'context is: ', context

    return context

actions = {
    'send': send,
    'getArticleSummary': get_article,
}

client = Wit(access_token=access_token, actions=actions)
client.interactive()
