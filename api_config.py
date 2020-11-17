import tweepy
from decouple import config

def create_api():
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    access_token = config('access_token')
    access_token_secret = config('access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api.verify_credentials()

    return api