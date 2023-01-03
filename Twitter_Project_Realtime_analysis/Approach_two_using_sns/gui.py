"""
This is a graphical interface for our application which user can put in the hashtag and the number of tweets and get the output!
"""
from analysis import Tweet_analysis_visual
import streamlit as st
import shutil
import time
from pathlib import Path
from PIL import Image
import pandas as pd
from datetime import date, timedelta


class VisualAnalysis:
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

        self.date_since = st.date_input(
            "from: ",  date.today() - timedelta(days=1))
        self.data_unitl = st.date_input("Until:  ", date.today())

    def fetch_tweet(self):
        if st.button('Fetch!'):
            if not self.hashtag:
                st.write("You did not enter the hashtag!")
            elif self.hashtag[0] == "#":
                d = Tweet_analysis_visual(
                    self.hashtag, self.limit, self.date_since, self.data_unitl)
                d.tweet_text_visuallization()
                len_data = len(d.data.tweet_catcher())
                if len_data < 40:
                    st.subheader(
                        "Sorry! There is not enough tweets containing your hashtag to be analyzed! :( \n ")
                    shutil.rmtree(d.data.path)

                else:
                    st.title("Your csv file is ready!")
                    df = pd.read_csv(
                        Path(d.data.path) / f'{self.hashtag}.csv')
                    st.write(df)

                    st.markdown("***")
                    st.subheader("Some basic EDA on your data!")
                    st.markdown(
                        f"In the following plots, you can see the most commonly used words, hashtags, and mentions in tweets containing your desired hashtag **{self.hashtag}**")
                    image_word = Image.open(
                        Path(d.data.path) / f'{self.hashtag}_words_frequencies.png')
                    st.image(image_word, caption='Word_frequencies')

                    st.markdown("***")
                    image_hash = Image.open(
                        Path(d.data.path) / f'{self.hashtag}_hashtags_frequencies.png')
                    st.image(image_hash, caption='Hashtag_frequencies')

                    st.markdown("***")
                    image_freq = Image.open(
                        Path(d.data.path) / f'{self.hashtag}_mentions_frequencies.png')
                    st.image(image_freq, caption='Mention_frequencies')

                    st.markdown("***")
                    st.title("Cleaned Tweets text!")
                    st.markdown(
                        "The following CSV file contains the cleaned format of tweets. Now It can be used for any NLP algorithm!")
                    df = pd.read_csv(
                        Path(d.data.path) / f'{self.hashtag}cleanedup.csv')
                    st.write(df)

                    st.markdown("***")
                    st.markdown(
                        f'The process is done! Your informaion is also saved at \" {d.data.path} \"  Folder for future use! \n')

            else:
                st.write(
                    f'{self.hashtag} is not acceptable. You shold Enter a Hashtag!')


handler = VisualAnalysis()
handler.fetch_tweet()
