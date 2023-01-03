import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd
from datetime import date, timedelta
from data_analysis import analysis
import time


class VisualAnalysis:
    st.title("Cheers!\nWelcome to our Twitter project for Python module!")
    st.markdown("Here's a very simple project that can pull tweets with a desired hashtag and produce some interesting data that can help you do more data analysis and natural language processing on Twitter!")
    image_tw = Image.open('twiiter.jpg')
    st.image(image_tw)
    st.markdown('##')

    def __init__(self):
        self.hashtag = st.selectbox("Below, you see the list of hashtags collected for this project. Please select one hashtag to see the relevant visual analysis: ",
                                    ("--Select Hashtag--", "#OpIran", "#IranRevolution",
                                     "#MahsaAmini", "#MohsenShekari", "#WomenLifeFreedom"))
        self.limit = st.slider(
            "Number of Tweets you want to catch:", 50, 50000, 50)

        self.date_since = str(st.date_input(
            "from: ", date(2022, 12, 20) - timedelta(days=5)))
        self.date_unitl = str(st.date_input("Until:  ", date(2022, 12, 20)))

        self.path = Path.cwd() / \
            f'{self.hashtag}_{self.limit}_Tweets_from_{self.date_since}_to_{self.date_unitl}_fetching_time_{time.strftime("%Y-%m-%d|%H:%M:%S")}'

    def fetch_tweet(self):
        if st.button('Fetch!'):
            df = analysis(self.hashtag, self.date_since,
                          self.date_unitl, self.limit)
            data = df.text_clean()
            st.title("Your csv file is ready!")
            st.write(data)
            st.markdown("***")

            st.subheader("Some basic EDA on your data!")
            st.markdown(
                f"In the following plots, you can see the most commonly used words, hashtags, and mentions in tweets containing your desired hashtag **{self.hashtag}**")

            df.text_analysis()
            image_word = Image.open(
                Path(self.path) / f'{self.hashtag}_Words_frequencies.png')
            st.image(image_word, caption='Word_frequencies')

            st.markdown("***")
            image_hash = Image.open(
                Path(self.path) / f'{self.hashtag}_Hashtags_frequencies.png')
            st.image(image_hash, caption='Hashtag_frequencies')

            st.markdown("***")
            image_freq = Image.open(
                Path(self.path) / f'{self.hashtag}_Mentions_frequencies.png')
            st.image(image_freq, caption='Mention_frequencies')

            st.markdown("***")
            st.title("Cleaned Tweets text!")
            st.markdown(
                "The following CSV file contains the cleaned format of tweets. Now It can be used for any NLP algorithm!")
            df = pd.read_csv(
                Path(self.path) / f'{self.hashtag}_text_cleanedup.csv')

            st.write(df)

            st.markdown("***")
            st.markdown(
                f'The process is done! Your informaion is also saved at \" {self.path} \"  Folder for future use! \n')


handler = VisualAnalysis()
handler.fetch_tweet()
