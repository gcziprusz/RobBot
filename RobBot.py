from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

import os
import time
import sys
import json
import hmac
import urllib
import pycurl
import hashlib
import StringIO
import re
import logging

def format_response_to_json(data):
    match = re.compile("\{(.+)\}$").search(data)
    return json.loads("{"+match.group(1)+"}")

if __name__ == '__main__':
    
    #Configure Logger
    logging.basicConfig(filename='RobBot.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    
    #Load keystore file from the HOME directory
    keystore_file = os.environ.get('HOME', '') + os.sep + '.rob_bot_keystore'
    
    #Read the API keys and other settings into variables
    OAUTH_TOKEN,OAUTH_TOKEN_SECRET,TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,AI_SECRET_KEY,AI_API_KEY,TWITTER_NAME,CHAT_BOT_ID,SNOOZE_TIME= file.readlines(open(keystore_file))
    
    if float(SNOOZE_TIME) < float(10):
        e= Exception("The SNOOZE_TIME IN YOUR keystore file has to be at least 10!!!") 
        logging.warning("Error: %s" % e)
        raise e
    
    twitter = Twitter(domain='search.twitter.com')
    twitter.uriparts=()

    last_id_replied = ''

    poster = Twitter(
        auth=OAuth(
            OAUTH_TOKEN.rstrip(), OAUTH_TOKEN_SECRET.rstrip(), TWITTER_CONSUMER_KEY.rstrip(), TWITTER_CONSUMER_SECRET.rstrip()),
        secure=True,
        api_version='1',
        domain='api.twitter.com')

    #Infinite loop to monitor the twitter account
    while True:
        try:
            results = twitter.search(q=TWITTER_NAME, since_id=last_id_replied)['results']
        
            if not results:
                logging.info("No tweets to "+TWITTER_NAME+" this time...")

            for result in results:
                question = result['text'].replace(TWITTER_NAME, '')
                asker = result['from_user']
                id = str(result['id'])
               
                logging.info(" Person who asked: " + asker + " and his question is: " + question)
                
                #Building json needed for the chatbot API
                messageJSON =json.dumps({
                                        'message': {
                                            'message': "'"+question.strip()+"'",
                                            'chatBotID': CHAT_BOT_ID,
                                            'timestamp': time.time()
                                        },
                                        'user': 
                                        {
                                            'externalID': "'"+asker+"'"
                                        }
                                        })
                #Hash needed for the chatbot API
                hash = hmac.new(AI_SECRET_KEY.rstrip(),messageJSON, hashlib.sha256).hexdigest()
                messageJSONencoded = urllib.quote_plus(messageJSON)
                url = "?apiKey="+AI_API_KEY.rstrip()+"&hash="+hash+"&message="+messageJSONencoded
                
                #Connect to the chatbot API and get response 
                conn = pycurl.Curl()
                conn.setopt(pycurl.TIMEOUT, 3)
                conn.setopt(pycurl.URL, 'http://www.personalityforge.com/api/chat/'+url)
                b = StringIO.StringIO()
                conn.setopt(pycurl.WRITEFUNCTION, b.write)
                conn.perform()
                conn.close()
                data = format_response_to_json(b.getvalue())
                msg = '@%s %s (%s)' % (asker, data['message']['message'], id[-4:])
                logging.info("Response: ")
                last_id_replied = id
                poster.statuses.update(status=msg)
        except Exception,e:
            logging.warning("Error: %s" % e)
        print "Running...(See log for more info)"
        logging.info("Snooze for "+SNOOZE_TIME+" seconds")
        time.sleep(float(SNOOZE_TIME))