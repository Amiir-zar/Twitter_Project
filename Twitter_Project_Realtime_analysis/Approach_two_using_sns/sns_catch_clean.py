import snscrape.modules.twitter as sntwitter
import pandas as pd
import csv
import re
import nltk.corpus
nltk.download('stopwords')
from nltk.corpus import stopwords
from pathlib import Path
import time 


class Tweet_analysis():
    """
    This is a class which contains two phases :
    cathcing the data from twitter and analysing the tweets
    Input   :   
    Search tweets according to keyword arguments specified using snscrape.

    Parameters
    ----------
    q (str): A query text to be matched.
    since (str. "yyyy-mm-dd"): A lower bound date (UTC) to restrict search. Default is 7 days before today.
    until (str. "yyyy-mm-dd"): An upper bound date (not included) to restrict search. Default is today.
    
    """

    def __init__(self, hashtag, limit,date_since, date_until):
        self.hashtag = hashtag
        self.limit = limit
        self.begin_date = date_since
        self.end_date = date_until
        path = Path.cwd() / \
            f'{self.hashtag}_{self.limit}_Tweets_from_{self.begin_date}_to_{self.end_date}_fetching_time_{time.strftime("%Y-%m-%d|%H:%M:%S")}'
        path.mkdir()
        self.path = f'./{self.hashtag}_{self.limit}_Tweets_from_{self.begin_date}_to_{self.end_date}_fetching_time_{time.strftime("%Y-%m-%d|%H:%M:%S")}'


    def tweet_catcher(self):
        """ 
        This function creates a csv file with this header 
        ["Username", "Text", "language",
        retweet_count", "Time", "location"]
        and fill it with most recent tweets containing a specific Hashtag(#)
        """
       
        # In the Next step we Create The out Csv file and add the headers to it:
        csvFile = open(f'{self.path}/{self.hashtag}.csv', 'a')
        csvWriter = csv.writer(csvFile)
        column_name = ["tweet_date","username", "user_location",
                       "tweet_retweetCount", "tweet_text" ]
        csvWriter.writerow(column_name)

        
        # Using TwitterSearchScraper to scrape data and append tweets to list
        criteria = f'{self.hashtag} since:{self.begin_date} until:{self.end_date} lang:"en" exclude:retweets exclude:replies '
        maxTweets = self.limit

        # We need to define a function to remove unnecessary NewLine in the text of the Tweets:
        def _remove_new_line(line: str):
            return line.replace("\n", "  ")

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(criteria).get_items()):
            if i > maxTweets:
                break
            csvWriter.writerow([tweet.date, tweet.user.username, tweet.user.location,
                               tweet.retweetCount, _remove_new_line(tweet.rawContent)])
        
            
        csvFile.close()
        return pd.read_csv(f'{self.path}/{self.hashtag}.csv')


    def text_cleaner(self,data):
        """ 
        This function analyses the information in the dataframe
        input : Tweet dataframe
        output : Cleaned text of tweets and Three graphs anlyzing the text of tweets ( most frequent words, most frequent mentions and most frequent hashtags )
        """

        csv_file = open(f'{self.path}/{self.hashtag}cleanedup.csv', 'a')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Text"])

        # normalizing (the loop) text by making it lowercase
        for index, row in data.iterrows():
            text = row['tweet_text'].lower()

            # 2. normalizing (loop body) the text by removing unicode characters
            text = re.sub(
                r"(\[A-Za-z0-9]+)|([^0-9A-Za-z#@ \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)     

            # 3.1 normalizing (loop body) the text by removing stopwords
            stop = stopwords.words('english')
            text = " ".join([word for word in text.split() if word not in stop])
            

            # 3.2 remove the below list fo words from the text
            to_be_removed_list = ["the", "this", "that", "by", "in", "on", "or", "of"]
            text_as_list = text.split()
            for word in to_be_removed_list:
                if word in text_as_list:
                    text_as_list.remove(word)

            # 3.3 rejoining the words from list to text
            text = " ".join([word for word in text_as_list])
            csv_writer.writerow([text])

        csv_file.close()
        return pd.read_csv(f'{self.path}/{self.hashtag}cleanedup.csv')

    