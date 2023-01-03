import time
from pathlib import Path
from nltk.corpus import stopwords
import tweepy as tw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import re
import string
import config
import csv
import nltk.corpus
nltk.download('stopwords')


class Tweet_analysis():
    """
    This is a class which contains two phases :
    cathcing the data from twitter and analysing the tweets
    Input   : The hastag we want to analyse and the limit of tweets to extract 
    output  : Three graphs ( most frequent words, most frequent mentions and most frequent hashtags )
    """

    def __init__(self, hashtag, limit):
        self.hashtag = hashtag
        self.limit = limit
        path = Path.cwd() / \
            f'{self.hashtag}_{self.limit}Tweets_{time.strftime("%Y-%m-%d|%H:%M:%S")}'
        path.mkdir()
        self.path = f'./{self.hashtag}_{self.limit}Tweets_{time.strftime("%Y-%m-%d|%H:%M:%S")}'

    def tweet_catchers(self):
        """ 
        This function creates a csv file with this header 
        ["Username", "Text", "language",
        retweet_count", "Time", "location"]
        and fill it with most recent tweets containing a specific Hashtag(#)
        """

        # First we will proceed to authorize ourselves with tweepys OAuthHandler.
        # NOTICE: For security we put the api in a separate file and put it in the .gitignore
        auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_key, config.access_secret)

        # We will now pass these authorization details to tweepy
        api = tw.API(auth, wait_on_rate_limit=True)

        # In the Next step we Create The out Csv file and add the headers to it:
        csvFile = open(f'{self.path}/{self.hashtag}.csv', 'a')
        csvWriter = csv.writer(csvFile)
        column_name = ["Username", "Text", "language",
                       "retweet_count", "Time", "location"]
        csvWriter.writerow(column_name)

        # We need to define a function to remove unnecessary NewLine in the text of the Tweets:

        def _remove_new_line(line: str):
            return line.replace("\n", "  ")

        try:
            # The Next for loop is kindda scary but all we are doing in it is :
            # We find the most recent tweets that contains The Hashtag and append it to the CSV file
            for tweet in tw.Cursor(api.search_tweets, q= {self.hashtag} , lang="en", tweet_mode='extended').items(self.limit):
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

        except BaseException as e:
            print('Status Failed On,', str(e))
            time.sleep(3)

        csvFile.close()
        return pd.read_csv(f'{self.path}/{self.hashtag}.csv')

    def analysis(self, data):
        """ 
        This function analyses the information in the dataframe
        input : Tweet dataframe
        output : Cleaned text of tweets and Three graphs anlyzing the text of tweets ( most frequent words, most frequent mentions and most frequent hashtags )
        """
        if data[data.columns[0]].count() < 40:
            pass

        else:

            csv_file = open(f'{self.path}/{self.hashtag}cleanedup.csv', 'a')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Text"])

            # normalizing (the loop) text by making it lowercase
            for index, row in data.iterrows():
                text = row['Text'].lower()

                # 2. normalizing (loop body) the text by removing unicode characters
                text = re.sub(
                    r"(\[A-Za-z0-9]+)|([^0-9A-Za-z#@ \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)

                # 3.1 normalizing (loop body) the text by removing stopwords
                stop = stopwords.words('english')
                text = " ".join(
                    [word for word in text.split() if word not in stop])

                # 3.2 remove the below list fo words from the text
                to_be_removed_list = ["the", "this",
                                      "that", "by", "in", "on", "or", "of"]
                text_as_list = text.split()
                for word in to_be_removed_list:
                    if word in text_as_list:
                        text_as_list.remove(word)

                # 3.3 rejoining the words from list to text
                text = " ".join([word for word in text_as_list])
                csv_writer.writerow([text])

            csv_file.close()
            data_cleaned = pd.read_csv(
                f'{self.path}/{self.hashtag}cleanedup.csv')

            # We add all of the rows in a string to be able count the numbers of words,hasthag and mentions
            final_text = data_cleaned['Text'].str.cat(sep='')

            # In the next step we split each words and store it in a list
            words_list = final_text.split()

            # Now we can loop over the words_list and seperate these three
            hashtags = []
            tags = []
            words = []
            for word in words_list:
                if word[0] == '#':
                    hashtags.append(word)
                elif word[0] == '@':
                    tags.append(word)
                else:
                    words.append(word)

            # Define a function as a counter to count each word,tag and hashtag
            def word_counter(word_list):
                d = {}
                for key in word_list:
                    d[key] = d.get(key, 0) + 1

            # Next, sort from highest to lowest.
                number_of_key = sorted(
                    d.items(), key=lambda x: x[1], reverse=True)

                return number_of_key

            top_25_word = dict(word_counter(words)[:25])
            top_25_hashtag = dict(word_counter(hashtags)[1:26])
            top_25_tags = dict(word_counter(tags)[:25])

            plt.figure(figsize=(20, 12))
            plt.xlabel('Word', fontsize=22)
            plt.ylabel('Freqeuncy', fontsize=22)
            plt.title(
                f'Each word Frequency in tweets contained {self.hashtag}', fontsize=24)
            plot = sns.barplot(x=list(top_25_word.keys()),
                               y=list(top_25_word.values()))
            plot.set_xticklabels(plot.get_xticklabels(),
                                 rotation=40, ha="right", fontsize='x-large')
            plt.savefig(f'{self.path}/{self.hashtag}_words_frequencies.png')

            plt.figure(figsize=(20, 12))
            plt.xlabel('Hashtag', fontsize=22)
            plt.ylabel('Freqeuncy', fontsize=22)
            plt.title(
                f'Each Hashtag Frequency in tweets contained {self.hashtag}', fontsize=24)
            plot = sns.barplot(x=list(top_25_hashtag.keys()),
                               y=list(top_25_hashtag.values()))
            plot.set_xticklabels(plot.get_xticklabels(),
                                 rotation=40, ha="right", fontsize='x-large')
            plt.savefig(f'{self.path}/{self.hashtag}_hashtags_frequencies.png')

            plt.figure(figsize=(20, 12))
            plt.xlabel('Tag', fontsize=22)
            plt.ylabel('Freqeuncy', fontsize=22)
            plt.title(
                f'Each tag Frequency in tweets contained {self.hashtag}', fontsize=24)
            plot = sns.barplot(x=list(top_25_tags.keys()),
                               y=list(top_25_tags.values()))
            plot.set_xticklabels(plot.get_xticklabels(),
                                 rotation=40, ha="right", fontsize='x-large')
            plt.savefig(f'{self.path}/{self.hashtag}_mentions_frequencies.png')
