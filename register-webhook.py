from decouple import config
from urllib.parse import quote_plus
from requests_oauthlib import OAuth1Session
import json


CONSUMER_KEY=config('consumer_key')
CONSUMER_SECRET=config('consumer_secret')
ACCESS_TOKEN=config('access_token')
ACCESS_TOKEN_SECRET=config('access_token_secret')


twitter = OAuth1Session(CONSUMER_KEY,
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)

webhook_endpoint = quote_plus('https://catfactbot-twitter.herokuapp.com/webhook/twitter')
url = f'https://api.twitter.com/1.1/account_activity/all/CatFactBot/webhooks.json?url={webhook_endpoint}'
r = twitter.post(url)

print(r.content)