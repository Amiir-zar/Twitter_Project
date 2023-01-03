"""
This is a graphical interface for our application which user can put in the hashtag and the number of tweets and get the output!
"""

from Twitt_class import Tweet_analysis
import streamlit as st
import shutil
import time
from pathlib import Path
from PIL import Image
import pandas as pd


class Graph_analysis:
    st.title("Tweet Catcher!")
    st.markdown("Here's a very simple project that can pull tweets with a desired hashtag and produce some interesting data that can help you do more data analysis and natural language processing on Twitter!")
    image_tw = Image.open('twiiter.jpg')
    st.image(image_tw)
    st.markdown('##')

    def __init__(self):
        self.hashtag = st.text_input(
            "Enter the #Hastag you want to see more information about ?(Ex. #amir) ")
        self.limit = st.slider(
            "Number of Tweets you want to catch:", 50, 10000, 50)

        self.path = Path(
            f'{self.hashtag}_{self.limit}Tweets_{time.strftime("%Y-%m-%d|%H:%M:%S")}')

    def fetch_tweet(self):

        if st.button('Fetch!'):
            if not self.hashtag:
                st.write("You did not enter the hashtag!")
            elif self.hashtag[0] == "#":
                analyze_class = Tweet_analysis(self.hashtag, self.limit)
                data = analyze_class.tweet_catchers()
                analyze_class.analysis(data)

                if data[data.columns[0]].count() < 40:
                    st.subheader(
                        "Sorry! There is not enough tweets containing your hashtag to be analyzed! :( \n ")
                    shutil.rmtree(self.path)

                else:
                    st.title("Your csv file is ready!")
                    df = pd.read_csv(
                        self.path / f'{self.hashtag}.csv').drop_duplicates(subset=["Text"])
                    st.write(df)

                    st.markdown("***")
                    st.subheader("Some basic EDA on your data!")
                    st.markdown(
                        f"In the following plots, you can see the most commonly used words, hashtags, and mentions in tweets containing your desired hashtag **{self.hashtag}**")
                    image_word = Image.open(
                        self.path / f'{self.hashtag}_words_frequencies.png')
                    st.image(image_word, caption='Words_frequencies')

                    st.markdown("***")
                    image_hash = Image.open(
                        self.path / f'{self.hashtag}_hashtags_frequencies.png')
                    st.image(image_hash, caption='Hashtags_frequencies')

                    st.markdown("***")
                    image_freq = Image.open(
                        self.path / f'{self.hashtag}_mentions_frequencies.png')
                    st.image(image_freq, caption='Mention_frequencies')

                    st.markdown("***")
                    st.title("Cleaned Tweets text!")
                    st.markdown(
                        "The following CSV file contains the cleaned format of tweets. Now It can be used for any NLP algorithm!")
                    df = pd.read_csv(
                        self.path / f'{self.hashtag}cleanedup.csv').drop_duplicates(subset=["Text"])
                    st.write(df)

                    st.markdown("***")
                    st.markdown(
                        f'The process is done! Your informaion is also saved at \" {self.hashtag}_{self.limit}Tweets_{time.strftime("%Y-%m-%d|%H:%M:%S")} \"  Folder for future use! \n')
            else:
                st.write(
                    f'{self.hashtag} is not acceptable. You shold Enter a Hashtag!')


a = Graph_analysis()
a.fetch_tweet()
