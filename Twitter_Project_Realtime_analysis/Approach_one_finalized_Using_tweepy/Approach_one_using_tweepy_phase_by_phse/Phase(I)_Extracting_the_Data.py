"""
This module extract the most recent tweets containing a specific Hashtag(#)
and put some information about in a csv file.

output:["Username", "Text", "language",
        retweet_count", "Time", "location"]
"""

import tweepy
import tweepy as tw
import pandas as pd
import csv
import re
import string
import preprocessor as p
import config


# First we will proceed to authorize ourselves with tweepys OAuthHandler.
# NOTICE: For security we put the api in a separate file and put it in the .gitignore
auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)


# We will now pass these authorization details to tweepy
api = tw.API(auth, wait_on_rate_limit=True)


# In the Next step we Create The out Csv file and add the headers to it:
csvFile = open('OpIran_new.csv', 'a')
csvWriter = csv.writer(csvFile)
column_name = ["Username", "Text", "language",
               "retweet_count", "Time", "location"]
csvWriter.writerow(column_name)


# Define the Hashtag we want to search
# Also we can get it from the user by
# search_words = input("please enter the Hashtag:")
new_search = "#HosseinRonaghi"

# We need to define a function to remove unnecessary NewLine in the text of the Tweets:


def _remove_new_line(line: str):
    return line.replace("\n", "  ")


# The Next for loop is kindda scary but all we are doing in it is :
# We find the most recent tweets that contains The Hashtag and append it to the CSV file :
for tweet in tweepy.Cursor(api.search_tweets, q=new_search, count=200, lang="en", tweet_mode='extended').items():
    twt_text = ""
    if hasattr(tweet, "retweeted_status"):
        try:
            twt_text = tweet.retweeted_status.extended_tweet["full_text"]
        except AttributeError:
            twt_text = tweet.retweeted_status.full_text

    else:
        try:
            twt_text = tweet.extended_tweet["full_text"]
        except AttributeError:
            twt_text = tweet.full_text
    # The scope of this project is to analyze only the english tweets so we filter only the en :
    csvWriter.writerow(
        [tweet.user.screen_name, _remove_new_line(twt_text), tweet.lang, tweet.retweet_count,
         tweet.created_at, tweet.user.location]
    )
