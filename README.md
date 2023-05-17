# Twitter-Project

The main objective of this project was to retrieve tweets from Twitter and provide users with relevant information about those tweets. 

## Description
In this project, we have developed a comprehensive system that involves fetching tweets from Twitter, analyzing their content, and presenting valuable information to users. To enhance the user experience, we have incorporated a user-friendly graphical user interface (GUI) using the Streamlit library. This GUI allows users to effortlessly interact with the system, select specific hashtags of interest, and retrieve insightful data from the tweets. 

We employ two major approaches for data acquisition: the real-time method and the data warehouse method. 

The real-time method involves users selecting a specific hashtag, and we utilize Tweepy or snscrape to fetch tweets containing that hashtag. These tweets are then analyzed to extract valuable insights.

To streamline the data retrieval process, we also implement the data warehouse method. This approach involves storing information related to various subjects in a data warehouse. By querying our databases, we can efficiently retrieve users' requested data, which significantly enhances the speed of analysis compared to the real-time method. However, it's important to note that constructing and maintaining a data warehouse incurs additional costs.

In the subsequent step, we focus on cleaning the text of the tweets to ensure they are in a suitable format for further analysis using natural language processing (NLP) models. This data cleaning step helps to remove any noise or irrelevant information, allowing us to derive more accurate insights from the text.


### Dependencies

* NLTK Library
* Tweepy
* Streamlit
* Pandas
* Seaborn

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
