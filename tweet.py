import pandas as pd
import tweepy
import time
import credentials
from os import environ
import subprocess


def main():
    consumer_key = credentials.API_KEY
    consumer_secret_key = credentials.API_SECRET_KEY
    access_token = credentials.ACCESS_TOKEN
    access_token_secret = credentials.ACCESS_TOKEN_SECRET


    interval = 15#60 * 60 * 24

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    while True:
        print('getting a random quote...')   
        yourtweet = subprocess.check_output(['python', 'select_quote.py'])
        yourtweet = yourtweet.decode('utf-8')
        print(yourtweet)
        tweet_ = yourtweet
        api.update_status(tweet_)
        time.sleep(interval) 



if __name__ == '__main__':
    main()