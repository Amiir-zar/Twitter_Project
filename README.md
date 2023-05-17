# Twitter-Project

The main objective of this project is to retrieve tweets from Twitter and provide users with analytical information about those tweets. For the first stage of this project we decided to show three bar chart( The most frequent word, Hashtag and mention) which contains a specific hashtag. 

## Description
In this project, we have developed a comprehensive system that involves fetching tweets from Twitter, analyzing their content, and presenting valuable information to users. To enhance the user experience, we have incorporated a user-friendly graphical user interface (GUI) using the Streamlit library. This GUI allows users to effortlessly interact with the system, select specific hashtags of interest, and retrieve insightful data from the tweets. 

We employ two major approaches for data acquisition: the real-time method and the data warehouse method. 

The real-time method involves users selecting a specific hashtag, and we utilize Tweepy or snscrape to fetch tweets containing that hashtag. These tweets are then analyzed to extract valuable insights.

To streamline the data retrieval process, we also implement the data warehouse method. This approach involves storing information related to various subjects in a data warehouse. By querying our databases, we can efficiently retrieve users' requested data, which significantly enhances the speed of analysis compared to the real-time method. However, it's important to note that constructing and maintaining a data warehouse incurs additional costs.

In the subsequent step, we focus on cleaning the text of the tweets to ensure they are in a suitable format for further analysis using natural language processing (NLP) models. This data cleaning step helps to remove any noise or irrelevant information, allowing us to derive more accurate insights from the text.

In the End we should mention this is the first stage and we are looking forward to expand this project by adding more statistical and insight about the tweets with specific hashtag and also build NLP model for sentimental analysis on those tweets.

### Dependencies

* NLTK Library
* Tweepy
* snscrape
* Streamlit
* Pandas
* Seaborn
* Mathplotlib

## Help

For running the program : 
Clone the repo and run the following code in the file directory
```
streamlit run gui.py
```

## Authors

Amirhossein Zarabadipour

Fereshte Mohammadi



## Version History

* 0.1
    * Initial Release

## Notice 

For using Tweepy you need to create a Twitter Developer Account and API Keyin twitter and request for V2 access.
More Info on how to create a Twitter Developer Account  :
https://medium.com/@Nonso_Analytics/how-to-get-a-twitter-developer-account-and-api-key-a-beginners-guide-1c5c18765a9d
