import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import time
from pathlib import Path
from datetime import datetime
from nltk.corpus import stopwords
import time
import csv
import re
import nltk.corpus
nltk.download('stopwords')


class analysis():
    def __init__(self,hashtag,date_since,date_until,limit):
        self.hashtag = hashtag
        self.date_since = date_since
        self.date_until = date_until
        self.limit = limit
        self.path = Path.cwd() / \
            f'{self.hashtag}_{self.limit}_Tweets_from_{self.date_since}_to_{self.date_until}_fetching_time_{time.strftime("%Y-%m-%d|%H:%M:%S")}'
    


    def text_clean(self):
        """
        This function get the Text of the tweets, clean it , remove stop words, unicode characters
        :return: clean text of tweets
        """

        # creating/writing a csv file - calling the text as a column
        path = Path.cwd() / \
            f'{self.hashtag}_{self.limit}_Tweets_from_{self.date_since}_to_{self.date_until}_fetching_time_{time.strftime("%Y-%m-%d|%H:%M:%S")}'
        path.mkdir()
        csv_file = open(path / f'./{self.hashtag}_text_cleanedup.csv', 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Text"])

        # reading the original csv file and printing as a column
        df = pd.read_csv(
            f'../01-Raw_Data/{self.hashtag}.csv')
        df_date_filter = df[(pd.to_datetime(df['Time']) >= self.date_since) &
                            (pd.to_datetime(df['Time']) <= self.date_until)]
        df_date_filter_number_filter = df_date_filter.head(self.limit)

        # writing a loop for filtering the language to English, as well as extracting the Text of each Tweet

        #  1. normalizing (the loop) text by making it lowercase
        for index, row in df_date_filter_number_filter.iterrows():
            text = row['Text'].lower()

            # 2. normalizing (loop body) the text by removing unicode characters
            text = re.sub(
                r"([^0-9A-Za-z#@ \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", text)

            # 3.1 normalizing (loop body) the text by removing stopwords
            stop = stopwords.words('english')
            text = " ".join([word for word in text.split() if word not in stop])

            # 3.2 remove the below list fo words from the text
            to_be_removed_list = ["the", "this", "that",
                                "by", "in", "on", "or", "of", "thats"]
            text_as_list = text.split()
            for word in to_be_removed_list:
                if word in text_as_list:
                    text_as_list.remove(word)

            # 3.3 rejoining the words from list to text
            text = " ".join([word for word in text_as_list])
            csv_writer.writerow([text])

        csv_file.close()
        df_date_filter_number_filter.to_csv(self.path / f'./{self.hashtag}_filtered_data.csv')
        return df_date_filter_number_filter
   


    def text_analysis(self):
        """
        This function load and prepares data based on given hashtag. It sorts
        :param hashtag:
        :return:
        """
        df = pd.read_csv(self.path / f'./{self.hashtag}_text_cleanedup.csv')
        # We add all of the rows in a string:
        final_text = df['Text'].str.cat(sep='')

        # in the next step we separate each words
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
        top_25_mentions = dict(word_counter(tags)[:25])


        def plot_section(hashtag, var, x_lable):
            plt.figure(figsize=(20, 12))
            plt.title(f'Each {x_lable} Frequency in {hashtag} on the Twitter', fontsize=22)
            plot = sns.barplot(x=list(var.values()), y=list(var.keys()))
            plot.set_xticklabels(plot.get_xticklabels(), fontsize='x-large')
            plot.set_yticklabels(plot.get_yticklabels(), fontsize='x-large')
            plt.savefig(
                self.path / f'./{hashtag}_{x_lable}_frequencies.png')
            plt.show()

        plot_section(self.hashtag, top_25_word, 'Words')
        plot_section(self.hashtag, top_25_hashtag, 'Hashtags')
        plot_section(self.hashtag, top_25_mentions, 'Mentions')
        