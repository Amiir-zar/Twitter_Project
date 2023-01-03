# Twitter-Project
In this project, two major approaches are being used to analyze the text of tweets with a desired hashtag. 
A Real-time approach is one where the user chooses their hashtag, and we use Tweepy or snscrape to search for tweets with the hashtag they need.  According to this approach, catching the data from Twitter takes a lot of time (whether using Tweepy or snscrape), so another way to simplify this process should be found. This can be achieved by storing information on related subjects in a data warehouse, then querying our databases to retrieve users' requests, making this approach way faster than the first one. Even though this approach is faster, it's much more expensive since we need to build a data warehouse first.
To illustrate how a Data-Warehouse can be used, we have stored Twitter data about the Iranian Revolutionary movement in 2022: 
Data were extracted from 5 specific hashtags ["#MahsaAmini", "#OpIran", "#Iranrevolution2022", "#MohsenShekari", and "#WomenLifeFreedom"]
In the next step, we cleaned the tweets' text to prepare them for NLP analysis.  Following that, a simple GUI was created to allow users to choose which hashtags they wanted to discover more about. While this analysis is relatively simple, it could become more sophisticated in the future. 

