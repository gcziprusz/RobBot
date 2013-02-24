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

def format_response_to_json(data):
    match = re.compile("\{(.+)\}$").search(data)
    return json.loads("{"+match.group(1)+"}")

if __name__ == '__main__':
    keystore_file = os.environ.get('HOME', '') + os.sep + '.rob_bot_keystore'
    
    OAUTH_TOKEN,OAUTH_TOKEN_SECRET,TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,AI_SECRET_KEY,AI_API_KEY,TWITTER_NAME = file.readlines(open(keystore_file))
    
    twitter = Twitter(domain='search.twitter.com')
    twitter.uriparts=()

    last_id_replied = ''

    if len(sys.argv) > 1:
        last_id_replied = sys.argv[1]

    poster = Twitter(
        auth=OAuth(
            OAUTH_TOKEN.rstrip(), OAUTH_TOKEN_SECRET.rstrip(), TWITTER_CONSUMER_KEY.rstrip(), TWITTER_CONSUMER_SECRET.rstrip()),
        secure=True,
        api_version='1',
        domain='api.twitter.com')

    while True:
        results = twitter.search(q=TWITTER_NAME, since_id=last_id_replied)['results']
        
        if not results:
            print 'No results this time...'

        for result in results:
                question = result['text'].replace(TWITTER_NAME, '')
                asker = result['from_user']
                id = str(result['id'])
                print " <<< " + asker + ": " + question
        
                messageJSON =json.dumps({
                                        'message': {
                                            'message': "'"+question.strip()+"'",
                                            'chatBotID': 6,
                                            'timestamp': time.time()
                                        },
                                        'user': 
                                        {
                                            'externalID': "'"+asker+"'"
                                        }
                                        })
                hash = hmac.new(AI_SECRET_KEY.rstrip(),messageJSON, hashlib.sha256).hexdigest()
                messageJSONencoded = urllib.quote_plus(messageJSON)
                url = "?apiKey="+AI_API_KEY.rstrip()+"&hash="+hash+"&message="+messageJSONencoded
                
                conn = pycurl.Curl()
                conn.setopt(pycurl.URL, 'http://www.personalityforge.com/api/chat/'+url)
                b = StringIO.StringIO()
                conn.setopt(pycurl.WRITEFUNCTION, b.write)
                conn.perform()
                conn.close()
                data = format_response_to_json(b.getvalue())
                msg = '@%s %s (%s)' % (asker, data['message']['message'], id[-4:])
                print '====> Resp = %s' % msg
               
                last_id_replied = id
                poster.statuses.update(status=msg)
        print 'Now sleeping... \n\n'
        time.sleep(20)