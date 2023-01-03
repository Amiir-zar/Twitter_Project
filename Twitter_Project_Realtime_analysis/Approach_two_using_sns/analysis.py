import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sns_catch_clean import Tweet_analysis

class Tweet_analysis_visual():


    def __init__(self, hashtag, limit, date_since, date_until):
        self.hashtag = hashtag
        self.limit = limit
        self.begin_date = date_since
        self.end_date = date_until

        self.data = Tweet_analysis(self.hashtag, self.limit,
                            self.begin_date, self.end_date)

    def tweet_text_visuallization(self):
        csv_data = self.data.tweet_catcher()
        len_data = len(self.data.tweet_catcher())
        if len_data > 40:
            cleaned_text_csv = self.data.text_cleaner(csv_data)
            final_text = cleaned_text_csv['Text'].str.cat(sep='')
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
            top_25_mentions = dict(word_counter(tags)[:25])


            def plot_section(hashtag, var, x_lable):
                plt.figure(figsize=(20, 12))
                plt.title(f'Each {x_lable} Frequency in {hashtag} on the Twitter', fontsize=22)
                plot = sns.barplot(x=list(var.values()), y=list(var.keys()))
                plot.set_xticklabels(plot.get_xticklabels(), fontsize='x-large')
                plot.set_yticklabels(plot.get_yticklabels(), fontsize='x-large')
                plt.savefig(
                    f'{self.data.path}/{self.data.hashtag}_{x_lable}_frequencies.png')

            plot_section(self.hashtag, top_25_word, 'words')
            plot_section(self.hashtag, top_25_hashtag, 'Hashtags')
            plot_section(self.hashtag, top_25_mentions, 'Mentions')
            